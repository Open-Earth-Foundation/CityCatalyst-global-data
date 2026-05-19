#!/usr/bin/env python3
"""Shared utilities for the v1 atom-based pipeline (formerly v2).

Holds the small set of helpers that the atom extractor, matcher, scorer,
and batch runners all need.

Exports:
  - Document                — page/section/verbatim resolver over a markdown doc
  - render_template         — tiny {{var}}-style substitution for prompt templates
  - Action (dataclass)      — action record from actions.json (new JSON schema)
  - load_document, load_actions, load_registry
  - RunStats, build_pairs, print_status — batch-runner infrastructure
  - cost constants (gpt-4.1-mini list pricing)
  - DEFAULT_* path constants
"""

from __future__ import annotations

import json
import re
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

V1 = Path(__file__).resolve().parents[1]
REPO = V1.parents[1]

DEFAULT_MARKDOWN_DIR = V1 / "data" / "markdown"
DEFAULT_ACTIONS_JSON = V1 / "data" / "registry" / "actions.json"
DEFAULT_REGISTRY = V1 / "data" / "registry" / "source_documents.json"

PAGE_BREAK_RE = re.compile(r"<!--\s*page_break:\s*(\d+)\s*-->")
HEADING_RE = re.compile(r"^##+\s+(.+?)$", re.MULTILINE)
TEMPLATE_VAR_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")


# ----------------------------------------------------------------------------
# Document indexing
# ----------------------------------------------------------------------------

class Document:
    """Lightweight wrapper that resolves page + section from a character offset.

    Constructor parses page_break markers and ## section headings into ordered
    indexes. find_verbatim() also handles whitespace-normalised matching for
    robustness against an LLM collapsing whitespace.
    """

    def __init__(self, doc_id: str, text: str):
        self.doc_id = doc_id
        self.text = text
        self._page_index: list[tuple[int, int]] = [
            (m.end(), int(m.group(1))) for m in PAGE_BREAK_RE.finditer(text)
        ]
        self._section_index: list[tuple[int, str]] = [
            (m.start(), m.group(1).strip("* ")) for m in HEADING_RE.finditer(text)
        ]

    def page_for_offset(self, offset: int) -> int | None:
        current = None
        for off, page in self._page_index:
            if off > offset:
                break
            current = page
        return current

    def section_for_offset(self, offset: int) -> str | None:
        current = None
        for off, sec in self._section_index:
            if off > offset:
                break
            current = sec
        return current

    def find_verbatim(self, needle: str) -> int | None:
        """Return character offset of `needle` in self.text, or None.
        Whitespace-normalised match for robustness against the LLM collapsing whitespace.
        """
        idx = self.text.find(needle)
        if idx >= 0:
            return idx
        norm_needle = re.sub(r"\s+", " ", needle).strip()
        if not norm_needle:
            return None
        norm_doc = re.sub(r"\s+", " ", self.text)
        idx = norm_doc.find(norm_needle)
        if idx < 0:
            return None
        # Map back to original offset
        collapsed = 0
        for orig_off, ch in enumerate(self.text):
            if collapsed >= idx:
                return orig_off
            if not (ch.isspace() and orig_off > 0 and self.text[orig_off - 1].isspace()):
                collapsed += 1
        return 0


def load_document(markdown_dir: Path, doc_id: str) -> Document:
    md = markdown_dir / doc_id / "document.md"
    if not md.exists():
        raise FileNotFoundError(f"No markdown for {doc_id}: {md}")
    return Document(doc_id, md.read_text(encoding="utf-8"))


# ----------------------------------------------------------------------------
# Actions and registry
# ----------------------------------------------------------------------------

@dataclass
class Action:
    action_id: str
    action_name: str
    description: str
    action_gpc_reference: str
    intervention_summary: str
    outcome_summary: str


def load_actions(json_path: Path) -> dict[str, Action]:
    """Read the actions registry. v1 schema: a JSON array of action objects
    with camelCase keys (`actionId`, `actionName`, ...) and nested
    `emissions.gpc_reference_number` for the GPC sector reference.

    For backwards compatibility this still accepts the legacy CSV at
    data/derived/actions_profiled.csv if pointed at one — detected by suffix.
    """
    actions: dict[str, Action] = {}

    if json_path.suffix == ".csv":
        import csv as _csv
        with json_path.open(encoding="utf-8-sig", newline="") as f:
            for row in _csv.DictReader(f):
                aid = (row.get("action_id") or "").strip()
                if not aid:
                    continue
                actions[aid] = Action(
                    action_id=aid,
                    action_name=(row.get("action_name") or "").strip(),
                    description=(row.get("description") or "").strip(),
                    action_gpc_reference=(row.get("gpc_reference") or "").strip(),
                    intervention_summary=(row.get("intervention_summary") or "").strip(),
                    outcome_summary=(row.get("outcome_summary") or "").strip(),
                )
        return actions

    data = json.loads(json_path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "actions" in data:
        data = data["actions"]
    if not isinstance(data, list):
        raise ValueError(f"unexpected actions.json shape at {json_path}: not a list")

    for row in data:
        aid = (row.get("actionId") or row.get("action_id") or "").strip()
        if not aid:
            continue
        # gpc_reference lives at emissions.gpc_reference_number (a list); take the first entry
        gpc = ""
        emissions = row.get("emissions") or {}
        refs = emissions.get("gpc_reference_number") if isinstance(emissions, dict) else None
        if refs:
            gpc = (refs[0] if isinstance(refs, list) else str(refs)).strip()
        actions[aid] = Action(
            action_id=aid,
            action_name=(row.get("actionName") or row.get("action_name") or "").strip(),
            description=(row.get("description") or "").strip(),
            action_gpc_reference=gpc,
            intervention_summary=(row.get("intervention_summary") or "").strip(),
            outcome_summary=(row.get("outcome_summary") or "").strip(),
        )
    return actions


def load_registry(registry_path: Path) -> dict[str, dict]:
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    return {e["source_document_id"]: e for e in data.get("source_documents", [])}


# ----------------------------------------------------------------------------
# Prompt template rendering
# ----------------------------------------------------------------------------

def render_template(template: str, vars: dict[str, str]) -> str:
    """Tiny Jinja-style {{ name }} substitution. Comments {# ... #} are stripped."""
    text = re.sub(r"\{#.*?#\}", "", template, flags=re.DOTALL)

    def sub(m: re.Match) -> str:
        key = m.group(1)
        if key not in vars:
            raise KeyError(f"missing template var {key!r}")
        return str(vars[key])

    return TEMPLATE_VAR_RE.sub(sub, text)


# ----------------------------------------------------------------------------
# Batch-runner infrastructure (used by v2_batch_match.py and archived
# v2_batch_run.py). Cost constants reflect gpt-4.1-mini list pricing.
# ----------------------------------------------------------------------------

INPUT_COST_PER_M = 0.40
CACHED_INPUT_COST_PER_M = 0.10
OUTPUT_COST_PER_M = 1.60

MIN_DOC_CHARS = 200
STATUS_EVERY = 50
MAX_RETRIES = 5


@dataclass
class RunStats:
    ok: int = 0
    fail: int = 0
    skip: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)

    def add_ok(self, inp: int, cached: int, out: int) -> None:
        with self.lock:
            self.ok += 1
            self.input_tokens += inp or 0
            self.cached_input_tokens += cached or 0
            self.output_tokens += out or 0

    def add_fail(self) -> None:
        with self.lock:
            self.fail += 1

    def add_skip(self) -> None:
        with self.lock:
            self.skip += 1

    @property
    def cost_usd(self) -> float:
        uncached = max(0, self.input_tokens - self.cached_input_tokens)
        return (
            uncached / 1_000_000 * INPUT_COST_PER_M
            + self.cached_input_tokens / 1_000_000 * CACHED_INPUT_COST_PER_M
            + self.output_tokens / 1_000_000 * OUTPUT_COST_PER_M
        )


def build_pairs(
    actions: dict[str, "Action"],
    doc_ids: list[str],
    action_filter: str | None,
    doc_filter: str | None,
    all_actions: bool,
    all_docs: bool,
) -> list[tuple["Action", str]]:
    """Return (action, doc_id) pairs ordered by document, then by action within
    document. This grouping keeps the document prefix warm in OpenAI's prefix
    cache as we walk through all actions for a doc before moving on.
    """
    if action_filter:
        if action_filter not in actions:
            raise SystemExit(f"unknown action: {action_filter}")
        action_list = [actions[action_filter]]
    elif all_actions:
        action_list = list(actions.values())
    else:
        raise SystemExit("Specify --action or --all-actions")

    if doc_filter:
        if doc_filter not in doc_ids:
            raise SystemExit(f"unknown or empty doc: {doc_filter}")
        doc_list = [doc_filter]
    elif all_docs:
        doc_list = doc_ids
    else:
        raise SystemExit("Specify --doc or --all-docs")

    return [(a, d) for d in doc_list for a in action_list]


def print_status(stats: RunStats, total: int, started: float) -> None:
    done = stats.ok + stats.fail + stats.skip
    elapsed = time.time() - started
    cached_pct = 0.0
    if stats.input_tokens:
        cached_pct = 100.0 * stats.cached_input_tokens / stats.input_tokens
    print(
        f"[{done}/{total}] ok={stats.ok} fail={stats.fail} skip={stats.skip} "
        f"in={stats.input_tokens:,} cached={stats.cached_input_tokens:,} ({cached_pct:.0f}%) "
        f"out={stats.output_tokens:,} cost=${stats.cost_usd:.2f} elapsed={elapsed/60:.1f}m",
        file=sys.stderr,
        flush=True,
    )
