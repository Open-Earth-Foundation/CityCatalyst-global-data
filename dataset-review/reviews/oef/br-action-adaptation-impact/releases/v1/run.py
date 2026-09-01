#!/usr/bin/env python3
"""Build the action-to-risk assessment as one JSON file."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input"
CACHE = ROOT / ".cache"
OUTPUT = ROOT / "output" / "action_risk_assessments.json"
ELIGIBILITY_PROMPT = ROOT / "prompts" / "eligibility.md"
EVIDENCE_PROMPT = ROOT / "prompts" / "evidence.md"
DEFAULT_MODEL = "gpt-5.6-terra"
LINK_CLAIMS = {"direct", "indirect", "no_link", "unclear"}
COMPONENTS = {"vulnerability", "exposure"}
OUTCOME_SIGNALS = {
    "strong_or_quantified",
    "moderate_or_conditional",
    "explicitly_limited",
    "strength_not_demonstrated",
    "not_applicable",
}
EFFECTIVENESS_LEVELS = {
    "high_effectiveness",
    "medium_effectiveness",
    "low_effectiveness",
    "no_demonstrated_effectiveness",
}

ELIGIBILITY_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "actions": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "action_id": {"type": "string"},
                    "claims": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "indicator_id": {"type": "string"},
                                "link_claim": {
                                    "type": "string",
                                    "enum": sorted(LINK_CLAIMS),
                                },
                                "rationale": {"type": "string"},
                            },
                            "required": ["indicator_id", "link_claim", "rationale"],
                        },
                    },
                },
                "required": ["action_id", "claims"],
            },
        }
    },
    "required": ["actions"],
}

EVIDENCE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "screening": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "source_id": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["evidence_found", "no_relevant_evidence"],
                    },
                },
                "required": ["source_id", "status"],
            },
        },
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "source_id": {"type": "string"},
                    "pdf_page": {"type": "integer"},
                    "quote": {"type": "string"},
                    "direction": {
                        "type": "string",
                        "enum": ["supports", "qualifies", "contradicts"],
                    },
                    "support_scope": {
                        "type": "string",
                        "enum": ["whole_action", "partial_action"],
                    },
                    "indicator_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "outcome_signal": {
                        "type": "string",
                        "enum": sorted(OUTCOME_SIGNALS),
                    },
                    "maladaptation_signal": {"type": "boolean"},
                },
                "required": [
                    "source_id",
                    "pdf_page",
                    "quote",
                    "direction",
                    "support_scope",
                    "indicator_ids",
                    "outcome_signal",
                    "maladaptation_signal",
                ],
            },
        },
    },
    "required": ["screening", "evidence"],
}

STOPWORDS = {
    "about", "after", "again", "against", "also", "among", "because", "been",
    "before", "being", "between", "both", "could", "from", "have", "into", "more",
    "most", "other", "over", "such", "than", "that", "their", "these", "they",
    "this", "through", "under", "using", "with", "within", "would", "ação", "ações",
    "para", "como", "com", "das", "dos", "uma", "por", "que", "sobre", "entre",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_id(prefix: str, *values: str) -> str:
    digest = hashlib.sha256("\x1f".join(values).encode()).hexdigest()[:16]
    return f"{prefix}_{digest}"


def review(row: dict[str, str]) -> dict[str, str | None]:
    return {
        "status": row.get("review_status") or "proposed",
        "note": row.get("review_note") or None,
        "reviewed_by": row.get("reviewed_by") or None,
        "reviewed_at": row.get("reviewed_at") or None,
    }


def load_inputs():
    actions = read_csv(INPUT / "actions.csv")
    indicators = read_csv(INPUT / "risk_framework.csv")
    sources = read_csv(INPUT / "sources.csv")
    require(len({row["action_id"] for row in actions}) == len(actions), "Duplicate action ID")
    require(
        len({row["indicator_id"] for row in indicators}) == len(indicators),
        "Duplicate indicator ID",
    )
    require(len({row["source_id"] for row in sources}) == len(sources), "Duplicate source ID")
    return actions, indicators, sources


def risk_structure(indicators: list[dict[str, str]]) -> list[dict[str, Any]]:
    sectors: dict[str, dict[str, Any]] = {}
    for row in indicators:
        sector = sectors.setdefault(row["sector"], {"sector": row["sector"], "risks": {}})
        risk = sector["risks"].setdefault(
            row["risk_id"],
            {"risk_id": row["risk_id"], "risk_name": row["risk_name"], "components": {}},
        )
        component = risk["components"].setdefault(
            row["component"], {"component": row["component"], "indicators": []}
        )
        component["indicators"].append(
            {
                "indicator_id": row["indicator_id"],
                "indicator_name": row["indicator_name"],
                "level": int(row["indicator_level"]),
                "pathway": [part.strip() for part in row["pathway"].split(">")],
            }
        )

    result = []
    for sector_name in sorted(sectors):
        sector = sectors[sector_name]
        risks = []
        for risk_id in sorted(sector["risks"]):
            risk = sector["risks"][risk_id]
            risk["components"] = [risk["components"][key] for key in sorted(risk["components"])]
            risks.append(risk)
        sector["risks"] = risks
        result.append(sector)
    return result


def source_registry(sources: list[dict[str, str]]) -> list[dict[str, Any]]:
    registry = []
    for row in sources:
        pdf = INPUT / "documents" / f"{row['source_id']}.pdf"
        page_count = None
        sha256 = None
        if pdf.exists():
            sha256 = file_hash(pdf)
            info = subprocess.run(
                ["pdfinfo", str(pdf)], check=True, capture_output=True, text=True
            ).stdout
            match = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
            page_count = int(match.group(1)) if match else None
        registry.append(
            {
                "source_id": row["source_id"],
                "legacy_source_ids": split_values(row["legacy_source_ids"]),
                "sectors": split_values(row["sectors"]),
                "title": row["title"],
                "publisher": row["publisher"],
                "publication_year": int(row["publication_year"]) if row["publication_year"] else None,
                "scope": row["scope"],
                "url": row["url"],
                "tier": row["tier"],
                "access_status": row["access_status"],
                "pdf": {
                    "path": f"input/documents/{row['source_id']}.pdf" if pdf.exists() else None,
                    "sha256": sha256,
                    "page_count": page_count,
                },
                "review": review(row),
            }
        )
    return registry


def empty_output(actions, indicators, sources) -> dict[str, Any]:
    return {
        "schema_version": "2.2.0",
        "release": "v1",
        "status": "eligibility_not_run",
        "definitions": {
            "direct": "The action's primary mechanism directly changes the indicator; eligible.",
            "indirect": "A secondary effect or co-benefit; recorded but not eligible.",
            "no_link": "No credible relationship. Omitted from action claims when screening is complete.",
            "unclear": "Directness cannot be determined from the supplied definitions.",
        },
        "summary": {},
        "risk_framework": risk_structure(indicators),
        "sources": source_registry(sources),
        "actions": [
            {
                "action_id": row["action_id"],
                "action_name": row["action_name"],
                "action_definition": row["action_definition"],
                "action_subcategory": row["action_subcategory"],
                "action_type": row["action_type"],
                "time_horizon": row["time_horizon"],
                "indicator_screening": {
                    "complete": False,
                    "implicit_no_link": True,
                    "method": None,
                    "model": None,
                    "prompt_version": None,
                },
                "indicator_claims": [],
                "source_screening": [],
                "component_claims": [],
                "evidence": [],
                "review": {
                    "status": "proposed",
                    "note": None,
                    "reviewed_by": None,
                    "reviewed_at": None,
                },
            }
            for row in actions
        ],
    }


def update_summary(data: dict[str, Any]) -> None:
    claims = [claim for action in data["actions"] for claim in action["indicator_claims"]]
    evidence = [item for action in data["actions"] for item in action["evidence"]]
    component_claims = [item for action in data["actions"] for item in action["component_claims"]]
    screening_groups = [item for action in data["actions"] for item in action["source_screening"]]
    counts = Counter(claim["link_claim"] for claim in claims)
    data["summary"] = {
        "action_count": len(data["actions"]),
        "indicator_count": sum(
            len(component["indicators"])
            for sector in data["risk_framework"]
            for risk in sector["risks"]
            for component in risk["components"]
        ),
        "source_count": len(data["sources"]),
        "direct_indicator_claim_count": counts["direct"],
        "indirect_indicator_claim_count": counts["indirect"],
        "unclear_indicator_claim_count": counts["unclear"],
        "component_claim_count": len(component_claims),
        "source_screening_group_count": len(screening_groups),
        "source_screening_record_count": sum(len(row["sources"]) for row in screening_groups),
        "evidence_record_count": len(evidence),
    }


def indicator_index(indicators: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["indicator_id"]: row for row in indicators}


def validate(data: dict[str, Any], actions, indicators, sources) -> None:
    action_ids = {row["action_id"] for row in actions}
    source_ids = {row["source_id"] for row in sources}
    source_by_id = {row["source_id"]: row for row in sources}
    indicator_by_id = indicator_index(indicators)
    require(data["schema_version"] in {"2.1.0", "2.2.0"}, "Unexpected output schema version")
    require({row["action_id"] for row in data["actions"]} == action_ids, "Action coverage mismatch")
    require({row["source_id"] for row in data["sources"]} == source_ids, "Source coverage mismatch")

    all_evidence_ids = []
    for action in data["actions"]:
        claims = action["indicator_claims"]
        claim_ids = [row["indicator_id"] for row in claims]
        require(len(claim_ids) == len(set(claim_ids)), f"Duplicate indicator claim: {action['action_id']}")
        direct_ids = set()
        strict_model_screen = action["indicator_screening"]["method"] == "model_indicator_screen"
        for claim in claims:
            indicator = indicator_by_id.get(claim["indicator_id"])
            require(indicator is not None, f"Unknown indicator claim: {claim['indicator_id']}")
            require(claim["link_claim"] in LINK_CLAIMS - {"no_link"}, "no_link claims must be implicit")
            require(bool(claim["rationale"]), f"Claim has no rationale: {action['action_id']}")
            if claim["link_claim"] == "direct":
                direct_ids.add(claim["indicator_id"])
                if strict_model_screen:
                    speculative = re.search(
                        r"\b(may|might|could|plausible|indirect|co-benefit)\b",
                        claim["rationale"],
                        flags=re.IGNORECASE,
                    )
                    require(
                        speculative is None,
                        f"Direct claim uses non-direct language: {action['action_id']}/{claim['indicator_id']}",
                    )

        screening_keys = set()
        for screening in action["source_screening"]:
            require(screening["component"] in COMPONENTS, "Invalid screening component")
            screening_keys.add(
                (screening["sector"], screening["risk_id"], screening["component"])
            )
            for result in screening["sources"]:
                require(result["source_id"] in source_ids, "Unknown screened source")
                require(
                    screening["sector"] in split_values(source_by_id[result["source_id"]]["sectors"]),
                    "Screened source is assigned to another sector",
                )
        require(
            len(screening_keys) == len(action["source_screening"]),
            "Duplicate source-screening group",
        )

        evidence_ids = {row["evidence_id"] for row in action["evidence"]}
        require(len(evidence_ids) == len(action["evidence"]), "Duplicate evidence ID within action")
        all_evidence_ids.extend(evidence_ids)
        for item in action["evidence"]:
            require(item["source_id"] in source_ids, f"Unknown evidence source: {item['evidence_id']}")
            require(item["pdf_page"] > 0 and bool(item["quote"]), f"Invalid evidence: {item['evidence_id']}")
            require(
                bool(item["indicator_ids"]) and set(item["indicator_ids"]) <= direct_ids,
                f"Evidence must reference at least one direct indicator: {item['evidence_id']}",
            )
            require(
                all(
                    indicator_by_id[indicator_id]["sector"] == item["sector"]
                    and indicator_by_id[indicator_id]["risk_id"] == item["risk_id"]
                    and indicator_by_id[indicator_id]["component"] == item["component"]
                    for indicator_id in item["indicator_ids"]
                ),
                f"Evidence indicator is in another sector, risk or component: {item['evidence_id']}",
            )
            if data["schema_version"] == "2.2.0":
                require(
                    item.get("outcome_signal") in OUTCOME_SIGNALS,
                    f"Evidence has no valid outcome signal: {item['evidence_id']}",
                )
                require(
                    (item["direction"] == "contradicts")
                    == (item["outcome_signal"] == "not_applicable"),
                    f"Contradicting evidence must use not_applicable: {item['evidence_id']}",
                )

        component_keys = set()
        for claim in action["component_claims"]:
            require(claim["component"] in COMPONENTS, "Invalid component claim")
            require(set(claim["direct_indicator_ids"]) <= direct_ids, "Component has non-direct indicators")
            require(set(claim["evidence_ids"]) <= evidence_ids, "Component references unknown evidence")
            allowed_effectiveness = (
                EFFECTIVENESS_LEVELS
                if data["schema_version"] == "2.2.0"
                else {"supported", "partially_supported", "not_demonstrated", "contradicted"}
            )
            require(
                claim["effectiveness"] in allowed_effectiveness,
                f"Invalid component effectiveness: {claim['effectiveness']}",
            )
            key = (claim["sector"], claim["risk_id"], claim["component"])
            component_keys.add(key)
            require(
                all(
                    (
                        indicator_by_id[indicator_id]["sector"],
                        indicator_by_id[indicator_id]["risk_id"],
                        indicator_by_id[indicator_id]["component"],
                    )
                    == key
                    for indicator_id in claim["direct_indicator_ids"]
                ),
                "Component claim contains an indicator from another risk",
            )
        require(
            len(component_keys) == len(action["component_claims"]),
            "Duplicate component claim",
        )

        expected_component_keys = {
            (
                indicator_by_id[indicator_id]["sector"],
                indicator_by_id[indicator_id]["risk_id"],
                indicator_by_id[indicator_id]["component"],
            )
            for indicator_id in direct_ids
        }
        if action["component_claims"]:
            require(component_keys == expected_component_keys, "Component claim coverage mismatch")
        if data["status"] == "proposed_human_review_pending":
            require(screening_keys == expected_component_keys, "Source screening coverage mismatch")

    require(len(all_evidence_ids) == len(set(all_evidence_ids)), "Duplicate evidence ID")
    stored_summary = dict(data.get("summary") or {})
    update_summary(data)
    if stored_summary:
        require(stored_summary == data["summary"], "Stored summary does not match the records")


def model_call(prompt, context, schema, *, name, args):
    key_material = json.dumps(
        {
            "prompt": prompt,
            "context": context,
            "schema": schema,
            "model": args.model,
            "reasoning_effort": args.reasoning_effort,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    cache_key = hashlib.sha256(key_material.encode()).hexdigest()
    cache_path = CACHE / "model_responses" / f"{name}_{cache_key}.json"
    if cache_path.exists() and not args.force:
        return json.loads(cache_path.read_text(encoding="utf-8"))["payload"]
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is required for model stages.")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit("Install the openai package before running model stages.") from exc

    response = OpenAI().responses.create(
        model=args.model,
        reasoning={"effort": args.reasoning_effort},
        instructions=prompt,
        input=context,
        text={
            "format": {
                "type": "json_schema",
                "name": name,
                "schema": schema,
                "strict": True,
            }
        },
        store=False,
    )
    require(response.status == "completed" and bool(response.output_text), f"Incomplete response: {name}")
    payload = json.loads(response.output_text)
    write_json(
        cache_path,
        {
            "response_id": response.id,
            "model": args.model,
            "usage": response.usage.model_dump() if response.usage else {},
            "payload": payload,
        },
    )
    return payload


def eligibility_context(sector, action_batch, sector_indicators):
    return json.dumps(
        {
            "sector": sector,
            "actions": [
                {
                    "action_id": row["action_id"],
                    "action_name": row["action_name"],
                    "action_definition": row["action_definition"],
                }
                for row in action_batch
            ],
            "indicators": [
                {
                    "indicator_id": row["indicator_id"],
                    "risk_name": row["risk_name"],
                    "component": row["component"],
                    "indicator_name": row["indicator_name"],
                    "pathway": row["pathway"],
                }
                for row in sector_indicators
            ],
        },
        ensure_ascii=False,
        indent=2,
    )


def run_eligibility(args, actions, indicators, sources):
    prompt = ELIGIBILITY_PROMPT.read_text(encoding="utf-8")
    sectors = sorted({row["sector"] for row in indicators})
    expected_calls = sum(
        (len(actions) + args.batch_size - 1) // args.batch_size for _ in sectors
    )
    if args.dry_run:
        print(json.dumps({"stage": "eligibility", "model_calls": expected_calls}))
        return None

    output = empty_output(actions, indicators, sources)
    output_actions = {row["action_id"]: row for row in output["actions"]}
    lookup = indicator_index(indicators)
    for sector in sectors:
        sector_indicators = [row for row in indicators if row["sector"] == sector]
        expected_indicator_ids = {row["indicator_id"] for row in sector_indicators}
        for start in range(0, len(actions), args.batch_size):
            batch = actions[start : start + args.batch_size]
            print(f"Eligibility: {sector}, actions {start + 1}-{start + len(batch)}", flush=True)
            payload = model_call(
                prompt,
                eligibility_context(sector, batch, sector_indicators),
                ELIGIBILITY_SCHEMA,
                name="indicator_eligibility",
                args=args,
            )
            returned = {row["action_id"]: row for row in payload["actions"]}
            require(set(returned) == {row["action_id"] for row in batch}, "Eligibility action mismatch")
            for action in batch:
                claims = returned[action["action_id"]]["claims"]
                returned_ids = [row["indicator_id"] for row in claims]
                require(
                    len(returned_ids) == len(set(returned_ids))
                    and set(returned_ids) == expected_indicator_ids,
                    f"Indicator coverage mismatch: {action['action_id']}/{sector}",
                )
                for claim in claims:
                    require(claim["link_claim"] in LINK_CLAIMS, "Invalid link claim")
                    if claim["link_claim"] == "no_link":
                        require(not claim["rationale"].strip(), "no_link rationale must be empty")
                        continue
                    indicator = lookup[claim["indicator_id"]]
                    output_actions[action["action_id"]]["indicator_claims"].append(
                        {
                            "indicator_id": claim["indicator_id"],
                            "link_claim": claim["link_claim"],
                            "rationale": claim["rationale"],
                            "review": {
                                "status": "proposed",
                                "note": None,
                                "reviewed_by": None,
                                "reviewed_at": None,
                            },
                        }
                    )
                    require(indicator["sector"] == sector, "Indicator sector mismatch")

    for action in output["actions"]:
        action["indicator_screening"] = {
            "complete": True,
            "implicit_no_link": True,
            "method": "model_indicator_screen",
            "model": args.model,
            "prompt_version": "1.0.0",
        }
    output["status"] = "eligibility_complete_evidence_pending"
    validate(output, actions, indicators, sources)
    write_json(OUTPUT, output)
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), **output["summary"]}))
    return output


def normalized_words(value: str) -> list[str]:
    value = unicodedata.normalize("NFKC", value).replace("\u00ad", "")
    value = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", value)
    return re.sub(r"[^\w]+", " ", value.casefold()).split()


def page_sections(text: str) -> dict[int, str]:
    parts = re.split(r"(?m)^## PDF page (\d+)\s*$", text)
    return {int(parts[index]): parts[index + 1] for index in range(1, len(parts), 2)}


def load_pages(source_id: str) -> dict[int, str]:
    cache_path = CACHE / "extracted_text" / f"{source_id}.md"
    if not cache_path.exists():
        pdf = INPUT / "documents" / f"{source_id}.pdf"
        require(pdf.exists(), f"PDF is unavailable: {source_id}")
        info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
        page_count = int(re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE).group(1))
        raw = subprocess.run(
            ["pdftotext", "-layout", str(pdf), "-"], check=True, capture_output=True
        ).stdout.decode("utf-8", errors="replace")
        pages = raw.split("\f")
        if len(pages) > page_count and not pages[-1].strip():
            pages.pop()
        pages.extend([""] * (page_count - len(pages)))
        require(len(pages) == page_count, f"PDF page split failed: {source_id}")
        lines = [f"# {source_id}", ""]
        for number, page in enumerate(pages, start=1):
            lines.extend([f"## PDF page {number}", "", page.rstrip(), ""])
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text("\n".join(lines), encoding="utf-8")
    return page_sections(cache_path.read_text(encoding="utf-8"))


def terms(value: str) -> set[str]:
    return {
        word
        for word in normalized_words(value)
        if len(word) >= 4 and word not in STOPWORDS and not word.isdigit()
    }


def candidate_pages(pages, action, sector, risk_name, direct_indicators, limit):
    action_terms = terms(action["action_name"] + " " + action["action_definition"])
    context_terms = terms(sector.replace("_", " ") + " " + risk_name)
    indicator_terms = terms(
        " ".join(row["indicator_name"] + " " + row["pathway"] for row in direct_indicators)
    )
    ranked = []
    for page_number, page_text in pages.items():
        page_terms = terms(page_text)
        score = (
            len(page_terms & action_terms)
            + 2 * len(page_terms & context_terms)
            + 2 * len(page_terms & indicator_terms)
        )
        if score:
            ranked.append((score, page_number, page_text[:6000]))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [
        {"pdf_page": page_number, "text": page_text}
        for _, page_number, page_text in ranked[:limit]
    ]


def grounding(quote: str, page_text: str) -> tuple[str, str]:
    quote_words = normalized_words(quote)
    page_words = normalized_words(page_text)
    require(bool(quote_words) and bool(page_words), "Empty quote or page")
    if " ".join(quote_words) in " ".join(page_words):
        return "verified_exact", "Normalized quote occurs on the cited PDF page."
    matcher = SequenceMatcher(None, quote_words, page_words, autojunk=False)
    blocks = matcher.get_matching_blocks()
    ordered_coverage = sum(block.size for block in blocks) / len(quote_words)
    if ordered_coverage >= 0.95:
        return "verified_ordered", f"Ordered token coverage is {ordered_coverage:.1%}."

    quote_counts = Counter(quote_words)
    page_counts = Counter(page_words)
    token_coverage = sum(
        min(count, page_counts[word]) for word, count in quote_counts.items()
    ) / len(quote_words)
    longest_block = max(block.size for block in blocks)
    minimum_anchor = min(5, max(2, len(quote_words) // 4))
    require(
        longest_block >= minimum_anchor
        and (token_coverage >= 0.98 or ordered_coverage >= 0.90),
        "Quote is not sufficiently present on the cited page "
        f"(ordered {ordered_coverage:.1%}, token {token_coverage:.1%})",
    )
    return (
        "layout_match",
        "Quote text is present but PDF layout changed its extraction order; "
        f"ordered coverage is {ordered_coverage:.1%} and token coverage is {token_coverage:.1%}.",
    )


def evidence_context(
    action, sector, risk_id, risk_name, component, direct_indicators, candidates
):
    return json.dumps(
        {
            "action": {
                "action_id": action["action_id"],
                "action_name": action["action_name"],
                "action_definition": action["action_definition"],
            },
            "sector": sector,
            "risk": {"risk_id": risk_id, "risk_name": risk_name},
            "component": component,
            "direct_indicators": [
                {
                    "indicator_id": row["indicator_id"],
                    "risk_name": row["risk_name"],
                    "indicator_name": row["indicator_name"],
                    "pathway": row["pathway"],
                }
                for row in direct_indicators
            ],
            "sources": candidates,
        },
        ensure_ascii=False,
        indent=2,
    )


def component_status(evidence_rows):
    positive = [row for row in evidence_rows if row["direction"] in {"supports", "qualifies"}]
    contradicting = [row for row in evidence_rows if row["direction"] == "contradicts"]
    rated = [
        row for row in positive
        if row.get("outcome_signal")
        in {"strong_or_quantified", "moderate_or_conditional", "explicitly_limited"}
    ]
    if not rated:
        if contradicting and not positive:
            reason = "The available evidence contradicts the expected effect."
        elif positive:
            reason = "Relevant evidence supports the direction of effect but does not demonstrate its effectiveness level."
        else:
            reason = "No relevant positive evidence was found in the screened source pages."
        return "no_demonstrated_effectiveness", reason

    signals = {row["outcome_signal"] for row in rated}
    has_context_limit = bool(contradicting) or any(
        row["direction"] == "qualifies" or row["support_scope"] == "partial_action"
        for row in rated
    )
    if signals == {"strong_or_quantified"} and not has_context_limit:
        return (
            "high_effectiveness",
            "Relevant evidence demonstrates a strong or quantified outcome for the direct component effect.",
        )
    if signals == {"explicitly_limited"} and not contradicting:
        return (
            "low_effectiveness",
            "Relevant evidence explicitly demonstrates a limited positive outcome.",
        )
    return (
        "medium_effectiveness",
        "Relevant evidence demonstrates a moderate, conditional, context-dependent or mixed positive outcome.",
    )


def build_component_claims(action, indicator_by_id):
    direct = [
        indicator_by_id[row["indicator_id"]]
        for row in action["indicator_claims"]
        if row["link_claim"] == "direct"
    ]
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for indicator in direct:
        key = (indicator["sector"], indicator["risk_id"], indicator["component"])
        groups.setdefault(key, []).append(indicator)
    claims = []
    for (sector, risk_id, component), group in sorted(groups.items()):
        ids = {row["indicator_id"] for row in group}
        related = [
            row
            for row in action["evidence"]
            if row["sector"] == sector
            and row["risk_id"] == risk_id
            and row["component"] == component
            and set(row["indicator_ids"]) & ids
        ]
        status, rationale = component_status(related)
        positive_sources = {
            row["source_id"]
            for row in related
            if row["direction"] in {"supports", "qualifies"}
        }
        coverage = (
            "none" if not positive_sources else "single_source" if len(positive_sources) == 1 else "multiple_sources"
        )
        claims.append(
            {
                "sector": sector,
                "risk_id": risk_id,
                "component": component,
                "direct_indicator_ids": sorted(ids),
                "effectiveness": status,
                "rationale": rationale,
                "source_coverage": coverage,
                "evidence_ids": [row["evidence_id"] for row in related],
                "review": {
                    "status": "proposed",
                    "note": None,
                    "reviewed_by": None,
                    "reviewed_at": None,
                },
            }
        )
    return claims


def run_evidence(args, actions, indicators, sources):
    require(OUTPUT.exists(), "Run eligibility before evidence.")
    data = json.loads(OUTPUT.read_text(encoding="utf-8"))
    validate(data, actions, indicators, sources)
    require(
        all(row["indicator_screening"]["complete"] for row in data["actions"]),
        "Eligibility screening is incomplete.",
    )
    action_input = {row["action_id"]: row for row in actions}
    indicator_by_id = indicator_index(indicators)
    groups = []
    for action in data["actions"]:
        direct = [
            indicator_by_id[row["indicator_id"]]
            for row in action["indicator_claims"]
            if row["link_claim"] == "direct"
        ]
        grouped_direct = {}
        for indicator in direct:
            grouped_direct.setdefault(
                (indicator["sector"], indicator["risk_id"], indicator["component"]), []
            ).append(indicator)
        groups.extend((action["action_id"], key, value) for key, value in grouped_direct.items())
    if args.dry_run:
        print(json.dumps({"stage": "evidence", "model_calls": len(groups)}))
        return None

    prompt = EVIDENCE_PROMPT.read_text(encoding="utf-8")
    for action in data["actions"]:
        action["source_screening"] = []
        action["component_claims"] = []
        action["evidence"] = []

    output_actions = {row["action_id"]: row for row in data["actions"]}
    for index, (action_id, (sector, risk_id, component), direct_indicators) in enumerate(
        groups, start=1
    ):
        action = action_input[action_id]
        risk_name = direct_indicators[0]["risk_name"]
        applicable = [
            row
            for row in sources
            if sector in split_values(row["sectors"])
            and row["access_status"] == "retrieved"
            and (INPUT / "documents" / f"{row['source_id']}.pdf").exists()
        ]
        candidates = []
        candidate_lookup = {}
        for source in applicable:
            selected = candidate_pages(
                load_pages(source["source_id"]),
                action,
                sector,
                risk_name,
                direct_indicators,
                args.pages_per_source,
            )
            candidates.append(
                {
                    "source_id": source["source_id"],
                    "source_title": source["title"],
                    "candidate_pages": selected,
                }
            )
            candidate_lookup[source["source_id"]] = {
                row["pdf_page"]: row["text"] for row in selected
            }

        print(
            f"Evidence {index}/{len(groups)}: "
            f"{action_id}/{sector}/{risk_id}/{component}",
            flush=True,
        )
        payload = model_call(
            prompt,
            evidence_context(
                action,
                sector,
                risk_id,
                risk_name,
                component,
                direct_indicators,
                candidates,
            ),
            EVIDENCE_SCHEMA,
            name="component_evidence",
            args=args,
        )
        source_ids = {row["source_id"] for row in applicable}
        screened_ids = [row["source_id"] for row in payload["screening"]]
        require(len(screened_ids) == len(set(screened_ids)) and set(screened_ids) == source_ids,
                f"Evidence screening coverage mismatch: "
                f"{action_id}/{sector}/{risk_id}/{component}")
        direct_ids = {row["indicator_id"] for row in direct_indicators}
        evidence_rows = []
        for item in payload["evidence"]:
            require(item["source_id"] in source_ids, "Evidence uses an unavailable source")
            require(set(item["indicator_ids"]) and set(item["indicator_ids"]) <= direct_ids,
                    "Evidence uses a non-direct indicator")
            page_text = candidate_lookup[item["source_id"]].get(item["pdf_page"])
            require(page_text is not None, "Evidence cites a page not supplied to the model")
            grounding_status, grounding_note = grounding(item["quote"], page_text)
            evidence_id = stable_id(
                "ev",
                action_id,
                risk_id,
                item["source_id"],
                str(item["pdf_page"]),
                item["quote"],
                item["direction"],
                *sorted(item["indicator_ids"]),
            )
            evidence_rows.append(
                {
                    "evidence_id": evidence_id,
                    "sector": sector,
                    "risk_id": risk_id,
                    "component": component,
                    "source_id": item["source_id"],
                    "pdf_page": item["pdf_page"],
                    "quote": item["quote"],
                    "direction": item["direction"],
                    "support_scope": item["support_scope"],
                    "indicator_ids": sorted(item["indicator_ids"]),
                    "outcome_signal": item["outcome_signal"],
                    "maladaptation_signal": item["maladaptation_signal"],
                    "grounding": {"status": grounding_status, "note": grounding_note},
                    "review": {
                        "status": "proposed",
                        "note": None,
                        "reviewed_by": None,
                        "reviewed_at": None,
                    },
                }
            )
        output_action = output_actions[action_id]
        output_action["evidence"].extend(evidence_rows)
        output_action["source_screening"].append(
            {
                "sector": sector,
                "risk_id": risk_id,
                "component": component,
                "status": "complete",
                "method": "lexical_page_candidates_and_model_review",
                "sources": [
                    {
                        **row,
                        "review": {
                            "status": "proposed",
                            "note": None,
                            "reviewed_by": None,
                            "reviewed_at": None,
                        },
                    }
                    for row in payload["screening"]
                ],
            }
        )

    for action in data["actions"]:
        action["component_claims"] = build_component_claims(action, indicator_by_id)
    data["schema_version"] = "2.2.0"
    data["status"] = "proposed_human_review_pending"
    update_summary(data)
    validate(data, actions, indicators, sources)
    write_json(OUTPUT, data)
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), **data["summary"]}))
    return data


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=["eligibility", "evidence", "all", "sync-sources", "validate"]
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--reasoning-effort", default="medium")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--pages-per-source", type=int, default=2)
    parser.add_argument("--force", action="store_true", help="Ignore cached model responses.")
    parser.add_argument("--dry-run", action="store_true", help="Report planned model calls only.")
    return parser.parse_args()


def main():
    args = parse_args()
    actions, indicators, sources = load_inputs()
    if args.command == "validate":
        require(OUTPUT.exists(), f"Output does not exist: {OUTPUT}")
        data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        validate(data, actions, indicators, sources)
        print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), **data["summary"], "status": "valid"}))
        return
    if args.command == "sync-sources":
        require(OUTPUT.exists(), f"Output does not exist: {OUTPUT}")
        data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        data["sources"] = source_registry(sources)
        data["status"] = "source_expansion_pending_evidence_rerun"
        data["source_expansion_note"] = (
            "The source registry has been refreshed. Newly retrieved documents have not yet "
            "been screened against the existing action-component assessments; run the evidence "
            "stage before producing the next human-review delivery."
        )
        update_summary(data)
        validate(data, actions, indicators, sources)
        write_json(OUTPUT, data)
        print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), **data["summary"]}))
        return
    if args.command in {"eligibility", "all"}:
        run_eligibility(args, actions, indicators, sources)
    if args.command in {"evidence", "all"}:
        run_evidence(args, actions, indicators, sources)


if __name__ == "__main__":
    main()
