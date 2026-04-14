import json
import os
import re
import time
import uuid
from datetime import datetime, timezone
from os import path
from urllib.parse import urlparse

import boto3
import requests
from mage_ai.data_preparation.shared.secrets import get_secret_value
from mage_ai.io.config import ConfigFileLoader
from mage_ai.settings.repo import get_repo_path
from pandas import DataFrame

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

PAGE_MARKER = re.compile(r"<!-- page_break: (\d+) -->")
HEADING_RE = re.compile(r"^#{1,4}\s+(.+)", re.MULTILINE)

SKIP_RULES = [
    r"^table of contents",
    r"abbreviations?|acronyms?",
    r"references?",
    r"bibliography",
]
SKIP_COMPILED = [re.compile(p, re.IGNORECASE) for p in SKIP_RULES]


def _resolve_aws_client_kwargs(config_loader: ConfigFileLoader) -> dict:
    config_dict = {}
    if hasattr(config_loader, "config") and isinstance(config_loader.config, dict):
        config_dict = config_loader.config
    elif hasattr(config_loader, "settings") and isinstance(config_loader.settings, dict):
        config_dict = config_loader.settings

    aws_access_key_id = config_dict.get("AWS_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = config_dict.get("AWS_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_session_token = config_dict.get("AWS_SESSION_TOKEN") or os.getenv("AWS_SESSION_TOKEN")
    region_name = config_dict.get("AWS_REGION") or os.getenv("AWS_REGION") or "us-east-1"

    kwargs = {"region_name": region_name}
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token:
        kwargs["aws_session_token"] = aws_session_token
    return kwargs


def _parse_s3_uri(s3_uri: str) -> tuple[str, str]:
    parsed = urlparse(s3_uri)
    if parsed.scheme != "s3" or not parsed.netloc or not parsed.path:
        raise ValueError(f"Invalid S3 URI: {s3_uri}")
    return parsed.netloc, parsed.path.lstrip("/")


def _load_prompt(kwargs: dict) -> str:
    prompt_path = kwargs.get("system_prompt_path", "prompts/policy-atom-extraction.txt")
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


def _parse_pages(markdown: str) -> dict[int, str]:
    pages = {}
    parts = PAGE_MARKER.split(markdown)
    it = iter(parts[1:])
    for page_num_str, page_text in zip(it, it):
        pages[int(page_num_str)] = page_text.strip()
    return pages


def _parse_sections(pages: dict[int, str]) -> list[dict]:
    headings = []
    for page_num in sorted(pages):
        for match in HEADING_RE.finditer(pages[page_num]):
            heading_text = match.group(1).strip().strip("*_")
            level = len(match.group(0)) - len(match.group(0).lstrip("#"))
            headings.append((page_num, level, heading_text))

    if not headings:
        return []

    sections = []
    last_page = sorted(pages.keys())[-1]

    for idx, (page_start, level, heading) in enumerate(headings):
        page_end = last_page
        for next_idx in range(idx + 1, len(headings)):
            if headings[next_idx][1] <= level:
                page_end = headings[next_idx][0] - 1
                break
        sections.append(
            {
                "heading": heading,
                "page_start": page_start,
                "page_end": max(page_start, page_end),
            }
        )
    return sections


def _is_relevant_heading(heading: str) -> bool:
    for pattern in SKIP_COMPILED:
        if pattern.search(heading):
            return False
    return True


def _relevant_pages(
    pages: dict[int, str],
    sections: list[dict],
    short_doc_threshold: int,
) -> list[tuple[int, str, str]]:
    min_chars = 50
    if not pages:
        return []

    if len(pages) < short_doc_threshold or not sections:
        return [
            (pn, text, "(full doc)")
            for pn, text in sorted(pages.items())
            if len(text.strip()) >= min_chars
        ]

    page_to_heading = {}
    for section in sections:
        for pn in range(section["page_start"], section["page_end"] + 1):
            page_to_heading[pn] = section["heading"]

    queue = []
    for pn in sorted(pages):
        text = pages[pn]
        heading = page_to_heading.get(pn)
        if len(text.strip()) < min_chars or not heading:
            continue
        if not _is_relevant_heading(heading):
            continue
        queue.append((pn, text, heading))
    return queue


def _batch_pages(queue: list[tuple[int, str, str]], batch_size: int) -> list[dict]:
    if not queue:
        return []

    batches = []
    current_pages = []
    current_heading = queue[0][2]

    for item in queue:
        page_num, page_text, heading = item
        is_same_section = heading == current_heading

        if current_pages and (not is_same_section or len(current_pages) >= batch_size):
            start = current_pages[0][0]
            end = current_pages[-1][0]
            merged = "\n\n".join(
                f"<!-- page_break: {pn} -->\n\n{txt}" for pn, txt, _ in current_pages
            )
            batches.append(
                {
                    "page_number": f"{start}-{end}" if start != end else str(start),
                    "page_text": merged,
                    "section_heading": current_heading,
                    "page_numbers": [pn for pn, _, _ in current_pages],
                }
            )
            current_pages = []
            current_heading = heading

        current_pages.append(item)
        current_heading = heading

    if current_pages:
        start = current_pages[0][0]
        end = current_pages[-1][0]
        merged = "\n\n".join(f"<!-- page_break: {pn} -->\n\n{txt}" for pn, txt, _ in current_pages)
        batches.append(
            {
                "page_number": f"{start}-{end}" if start != end else str(start),
                "page_text": merged,
                "section_heading": current_heading,
                "page_numbers": [pn for pn, _, _ in current_pages],
            }
        )
    return batches


def _extract_json_array(content: str) -> list[dict]:
    cleaned = re.sub(r"^```(?:json)?\s*", "", content.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        payload = json.loads(cleaned)
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
    except json.JSONDecodeError:
        pass
    return []


def _page_number_from_atom(atom: dict, fallback: int) -> int:
    match = re.search(r"Page\s+(\d+)", str(atom.get("page_or_section", "")), re.IGNORECASE)
    return int(match.group(1)) if match else fallback


def _call_extraction_api(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    payload: dict,
    timeout_seconds: int,
    max_retries: int = 2,
) -> list[dict]:
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
                        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
                    ],
                },
                timeout=timeout_seconds,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return _extract_json_array(content)
        except Exception as exc:
            if attempt < max_retries:
                wait = 2**attempt
                print(
                    f"API call failed (attempt {attempt + 1}/{max_retries + 1}): {exc} — retrying in {wait}s"
                )
                time.sleep(wait)
            else:
                raise


@data_exporter
def export_data_to_s3(df: DataFrame, **kwargs) -> DataFrame:
    """
    Read policy markdown files from S3, extract atoms via OpenAI, upload JSONL atoms to S3.
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_loader = ConfigFileLoader(config_path, "default")
    s3_client = boto3.client("s3", **_resolve_aws_client_kwargs(config_loader))

    destination_bucket = kwargs.get("destination_bucket", "test-global-api")
    destination_prefix = kwargs.get(
        "destination_prefix",
        "raw_data/cl-ssg/cl-ssg-policy-documents/releases/2026/markdown",
    ).strip("/")
    source_name = kwargs.get("source_name", "cl-ssg-policy-documents")
    model = kwargs.get("openai_model", "gpt-4.1-mini")
    short_doc_threshold = int(kwargs.get("short_doc_threshold", 40))
    batch_size = int(kwargs.get("batch_size", 4))
    sleep_seconds = float(kwargs.get("sleep_seconds", 0.25))
    timeout_seconds = int(kwargs.get("openai_timeout_seconds", 120))
    max_retries = int(kwargs.get("openai_max_retries", 2))
    atoms_file_extension = str(kwargs.get("atoms_file_extension", "jsonl")).strip(".").lower()
    if not atoms_file_extension:
        atoms_file_extension = "jsonl"

    api_key = get_secret_value("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for atom extraction.")

    system_prompt = _load_prompt(kwargs)

    if df is None or df.empty:
        print("No markdown files available for policy atom extraction.")
        return DataFrame(columns=["document_stem", "markdown_s3_uri", "atoms_s3_uri", "status"])

    output_rows = []
    converted = 0
    failed = 0

    for _, row in df.iterrows():
        document_stem = str(row.get("document_stem", "")).strip()
        markdown_s3_uri = row.get("markdown_s3_uri")
        pdf_s3_uri = row.get("pdf_s3_uri") or markdown_s3_uri
        atoms_s3_uri = None
        status = "failed"

        if not document_stem or not markdown_s3_uri:
            failed += 1
            output_rows.append(
                {
                    "document_stem": document_stem,
                    "markdown_s3_uri": markdown_s3_uri,
                    "atoms_s3_uri": atoms_s3_uri,
                    "status": "missing_input",
                }
            )
            continue

        try:
            markdown_bucket, markdown_key = _parse_s3_uri(str(markdown_s3_uri))
            source_obj = s3_client.get_object(Bucket=markdown_bucket, Key=markdown_key)
            markdown = source_obj["Body"].read().decode("utf-8")

            pages = _parse_pages(markdown)
            sections = _parse_sections(pages)
            queue = _relevant_pages(pages, sections, short_doc_threshold)
            batches = _batch_pages(queue, batch_size=batch_size)

            atoms = []
            for batch in batches:
                payload = {
                    "source_name": source_name,
                    "source_url": pdf_s3_uri,
                    "doc_id": document_stem,
                    "page_number": batch["page_number"],
                    "page_text": batch["page_text"],
                }
                extracted = _call_extraction_api(
                    api_key=api_key,
                    model=model,
                    system_prompt=system_prompt,
                    payload=payload,
                    timeout_seconds=timeout_seconds,
                    max_retries=max_retries,
                )
                fallback_page = batch["page_numbers"][0]
                for atom in extracted:
                    atom["_doc_id"] = document_stem
                    atom["_source_name"] = source_name
                    atom["_section"] = batch["section_heading"]
                    atom["_page_number"] = _page_number_from_atom(atom, fallback=fallback_page)
                    atom["_atom_id"] = str(uuid.uuid4())
                    atom["_extracted_at"] = datetime.now(timezone.utc).isoformat()
                    atoms.append(atom)

                time.sleep(sleep_seconds)

            atoms_key = f"{destination_prefix}/atoms/{document_stem}_atoms.{atoms_file_extension}"
            atoms_payload = "\n".join(json.dumps(atom, ensure_ascii=False) for atom in atoms)
            if atoms_payload:
                atoms_payload += "\n"

            s3_client.put_object(
                Bucket=destination_bucket,
                Key=atoms_key,
                Body=atoms_payload.encode("utf-8"),
                ContentType="application/jsonl",
            )
            atoms_s3_uri = f"s3://{destination_bucket}/{atoms_key}"
            converted += 1
            status = "converted"
            print(f"Extracted {len(atoms)} atoms for {document_stem} -> {atoms_s3_uri}")

        except Exception as exc:
            failed += 1
            print(f"Failed policy atom extraction for markdown_s3_uri={markdown_s3_uri}: {exc}")

        output_rows.append(
            {
                "document_stem": document_stem,
                "markdown_s3_uri": markdown_s3_uri,
                "atoms_s3_uri": atoms_s3_uri,
                "status": status,
            }
        )

    print(
        "Policy atom extraction complete: "
        f"converted={converted}, failed={failed}, total={len(df)}"
    )
    return DataFrame(output_rows)
