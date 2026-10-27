import json
import os
import re
import time
from datetime import datetime, timezone
from os import path

import boto3
import pandas as pd
import requests
from mage_ai.data_preparation.shared.secrets import get_secret_value
from mage_ai.io.config import ConfigFileLoader
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

DOC_TYPE_PRIORITY = {
    "completion_report": 4,
    "midterm_review": 3,
    "implementation_status": 3,
    "annual_performance": 2,
    "project_appraisal": 1,
    "funding_proposal": 1,
    "project_information": 1,
    "environmental_social": 1,
}

ATOM_FIELDS = [
    "primitive_type",
    "plain_language_summary",
    "raw_label",
    "raw_value_text",
    "raw_value_numeric",
    "raw_unit",
    "page_or_section",
    "source_name",
    "evidence_kind",
    "scope_hint",
    "intervention_ref",
    "notes",
]

TYPE_CAPS = {
    "financing": 30,
    "impact": 20,
    "performance": 20,
    "scale": 20,
    "intervention": 15,
    "implementation_insight": 15,
    "identity": 10,
    "timeline": 10,
}


def _resolve_aws_client_kwargs(config_loader: ConfigFileLoader) -> dict:
    """Build boto3 S3 client kwargs from config and environment."""
    config_dict = {}
    if hasattr(config_loader, "config") and isinstance(config_loader.config, dict):
        config_dict = config_loader.config
    elif hasattr(config_loader, "settings") and isinstance(config_loader.settings, dict):
        config_dict = config_loader.settings

    aws_access_key_id = config_dict.get("AWS_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = (
        config_dict.get("AWS_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    aws_session_token = config_dict.get("AWS_SESSION_TOKEN") or os.getenv("AWS_SESSION_TOKEN")
    region_name = config_dict.get("AWS_REGION") or os.getenv("AWS_REGION") or "us-east-1"

    kwargs = {"region_name": region_name}
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token:
        kwargs["aws_session_token"] = aws_session_token
    return kwargs


def _load_prompt(kwargs: dict) -> str:
    """Load the synthesis system prompt from the configured path."""
    prompt_path = kwargs.get("system_prompt_path", "prompts/project-atom-synthesis.txt")
    full_path = path.join(get_repo_path(), prompt_path)
    if not path.exists(full_path):
        raise FileNotFoundError(
            f"Prompt file not found at {full_path}. "
            "Set `system_prompt_path` to a valid prompt file."
        )
    with open(full_path, "r", encoding="utf-8") as file_obj:
        prompt = file_obj.read().strip()
    if not prompt:
        raise ValueError(f"Prompt file is empty: {full_path}")
    return prompt


def _read_atoms_from_s3(s3_client, bucket: str, key: str) -> list[dict]:
    """Parse a JSONL/NDJSON atom file from S3 into a list of dict rows."""
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read().decode("utf-8")
    atoms: list[dict] = []
    for line in body.splitlines():
        text = line.strip()
        if not text:
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            atoms.append(payload)
    return atoms


def _extract_json_object(content: str) -> dict:
    """Extract and parse a JSON object from model output."""
    cleaned = re.sub(r"^```(?:json)?\s*", "", content.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)
    payload = json.loads(cleaned)
    if not isinstance(payload, dict):
        raise ValueError("Synthesis model output must be a JSON object.")
    return payload


def _select_atoms(atoms_df: DataFrame) -> list[dict]:
    """Apply notebook selection rules and return capped atom payload rows."""
    if atoms_df is None or atoms_df.empty:
        return []

    df = atoms_df.copy()
    df["_sq"] = (df.get("evidence_kind", pd.Series("", index=df.index)) == "quantitative").astype(int)
    df["_sd"] = df.get("_doc_type", pd.Series("", index=df.index)).map(
        lambda value: DOC_TYPE_PRIORITY.get(str(value), 0)
    )
    if "raw_value_numeric" in df.columns:
        df["_sn"] = df["raw_value_numeric"].notna().astype(int)
    else:
        df["_sn"] = 0
    df = df.sort_values(["_sd", "_sq", "_sn"], ascending=False)

    rows = []
    for primitive_type, cap in TYPE_CAPS.items():
        rows.append(df[df["primitive_type"] == primitive_type].head(cap))
    combined = pd.concat(rows) if rows else df.iloc[0:0]

    for column in ATOM_FIELDS:
        if column not in combined.columns:
            combined[column] = ""
    return combined[ATOM_FIELDS].fillna("").to_dict(orient="records")


def _build_catalog_payload(row: dict) -> dict:
    """Map project_portfolio fields to the prompt's catalog payload schema."""
    return {
        "project_id": row.get("source_project_id"),
        "project_name": row.get("project_name"),
        "funder": row.get("source_name"),
        "country": row.get("country"),
        "country_code": row.get("country_code"),
        "sector": row.get("sector"),
        "instrument_type": None,
        "total_commitment_amount": row.get("total_commitment_amount"),
        "approval_date": row.get("approval_date"),
        "closing_date": row.get("closing_date"),
        "status": row.get("status"),
    }


def _call_synthesis_api(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    payload: dict,
    timeout_seconds: int,
    max_retries: int = 2,
) -> dict:
    """Call OpenAI chat completions and return parsed synthesis JSON."""
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": json.dumps(payload, ensure_ascii=False, default=str)},
                    ],
                },
                timeout=timeout_seconds,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return _extract_json_object(content)
        except Exception as exc:
            if attempt < max_retries:
                wait_seconds = 2**attempt
                print(
                    f"Synthesis API call failed (attempt {attempt + 1}/{max_retries + 1}): "
                    f"{exc} - retrying in {wait_seconds}s"
                )
                time.sleep(wait_seconds)
            else:
                raise


@data_exporter
def export_data_to_s3(df: DataFrame, **kwargs) -> DataFrame:
    """
    Read all atom JSONL files under each project's atoms/ prefix, synthesize one project JSON,
    and upload to the project's synthesis/ prefix in S3.
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_loader = ConfigFileLoader(config_path, "default")
    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))

    destination_bucket = kwargs.get("destination_bucket", "test-global-api")
    destination_prefix = kwargs.get(
        "destination_prefix",
        "raw_data/world_bank/world_bank_projects/documents",
    ).strip("/")
    synthesis_filename = kwargs.get("synthesis_filename", "project_synthesis.json").strip()
    model = kwargs.get("openai_model", "gpt-4.1")
    timeout_seconds = int(kwargs.get("openai_timeout_seconds", 180))
    max_retries = int(kwargs.get("openai_max_retries", 2))
    skip_if_synthesis_exists = bool(kwargs.get("skip_if_synthesis_exists", True))

    if df is None or df.empty:
        print("No projects available for synthesis.")
        return DataFrame(columns=["source_project_id", "atoms_count", "synthesis_s3_uri", "status"])

    api_key = get_secret_value("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for synthesis.")
    system_prompt = _load_prompt(kwargs)

    output_rows = []
    synthesized = 0
    skipped = 0
    failed = 0

    for _, row in df.iterrows():
        source_project_id = str(row.get("source_project_id", "")).strip()
        if not source_project_id:
            failed += 1
            output_rows.append(
                {
                    "source_project_id": source_project_id,
                    "atoms_count": 0,
                    "synthesis_s3_uri": None,
                    "status": "missing_project_id",
                }
            )
            continue

        synthesis_key = (
            f"{destination_prefix}/{source_project_id}/synthesis/{synthesis_filename}"
        ).strip("/")
        synthesis_s3_uri = f"s3://{destination_bucket}/{synthesis_key}"
        atoms_prefix = f"{destination_prefix}/{source_project_id}/atoms/"

        if skip_if_synthesis_exists:
            try:
                s3_client.head_object(Bucket=destination_bucket, Key=synthesis_key)
                skipped += 1
                output_rows.append(
                    {
                        "source_project_id": source_project_id,
                        "atoms_count": 0,
                        "synthesis_s3_uri": synthesis_s3_uri,
                        "status": "skipped_existing_synthesis",
                    }
                )
                continue
            except Exception:
                pass

        try:
            paginator = s3_client.get_paginator("list_objects_v2")
            atom_keys: list[str] = []
            for page in paginator.paginate(Bucket=destination_bucket, Prefix=atoms_prefix):
                for item in page.get("Contents", []):
                    key = item.get("Key", "")
                    if key.endswith(".jsonl") or key.endswith(".ndjson"):
                        atom_keys.append(key)

            atom_payloads: list[dict] = []
            for key in atom_keys:
                atom_payloads.extend(_read_atoms_from_s3(s3_client, destination_bucket, key))

            atoms_df = DataFrame(atom_payloads)
            selected_atoms = _select_atoms(atoms_df)
            if not selected_atoms:
                failed += 1
                output_rows.append(
                    {
                        "source_project_id": source_project_id,
                        "atoms_count": 0,
                        "synthesis_s3_uri": None,
                        "status": "no_atoms_found",
                    }
                )
                continue

            catalog_payload = _build_catalog_payload(row.to_dict())
            synthesis_input = {"catalog": catalog_payload, "evidence": selected_atoms}
            synthesis = _call_synthesis_api(
                api_key=api_key,
                model=model,
                system_prompt=system_prompt,
                payload=synthesis_input,
                timeout_seconds=timeout_seconds,
                max_retries=max_retries,
            )

            synthesis["_meta"] = {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "source_project_id": source_project_id,
                "selected_atoms_count": len(selected_atoms),
                "raw_atoms_count": len(atom_payloads),
                "model": model,
            }

            s3_client.put_object(
                Bucket=destination_bucket,
                Key=synthesis_key,
                Body=json.dumps(synthesis, ensure_ascii=False, indent=2).encode("utf-8"),
                ContentType="application/json",
            )

            synthesized += 1
            output_rows.append(
                {
                    "source_project_id": source_project_id,
                    "atoms_count": len(atom_payloads),
                    "synthesis_s3_uri": synthesis_s3_uri,
                    "status": "synthesized",
                }
            )
            print(
                f"Synthesized project {source_project_id} with {len(selected_atoms)} selected atoms "
                f"({len(atom_payloads)} raw) -> {synthesis_s3_uri}"
            )
        except Exception as exc:
            failed += 1
            print(f"Failed synthesis for source_project_id={source_project_id}: {exc}")
            output_rows.append(
                {
                    "source_project_id": source_project_id,
                    "atoms_count": 0,
                    "synthesis_s3_uri": None,
                    "status": "failed",
                }
            )

    print(
        "World Bank project synthesis complete: "
        f"synthesized={synthesized}, skipped={skipped}, failed={failed}, total={len(df)}"
    )
    return DataFrame(output_rows)
