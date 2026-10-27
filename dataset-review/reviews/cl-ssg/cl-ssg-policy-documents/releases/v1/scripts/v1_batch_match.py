#!/usr/bin/env python3
"""Batch runner for stage-2 atom matching (action x document).

Orders pairs by document then action for prefix-cache reuse on the shared
atoms block. Skips existing output JSON (resume-safe).

Usage:
  python v1_batch_match.py --all-actions --all-docs --dry-list
  python v1_batch_match.py --all-actions --all-docs --concurrency 16
  python v1_batch_match.py --all-actions --doc chl_parcc_arica --concurrency 4
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import v1_common as ef  # noqa: N812 — keeping `ef` alias for now to minimise diff
import v1_match_atoms_to_action as match

from v1_common import (
    INPUT_COST_PER_M,
    CACHED_INPUT_COST_PER_M,
    OUTPUT_COST_PER_M,
    MAX_RETRIES,
    STATUS_EVERY,
    RunStats,
    build_pairs,
    print_status,
)

V1 = Path(__file__).resolve().parents[1]
DEFAULT_ATOMS_DIR = V1 / "data" / "atoms"
DEFAULT_OUTPUT_DIR = V1 / "data" / "policy_action_signals"


def list_doc_ids_with_atoms(atoms_dir: Path, registry: dict[str, dict]) -> list[str]:
    out: list[str] = []
    for doc_id in sorted(registry):
        atoms_path = atoms_dir / f"{doc_id}.jsonl"
        if not atoms_path.exists():
            continue
        if atoms_path.stat().st_size < 10:
            continue
        if registry[doc_id].get("document_status") == "placeholder":
            continue
        out.append(doc_id)
    return out


def process_pair(
    action: ef.Action,
    doc_id: str,
    doc_meta: dict,
    atoms_dir: Path,
    output_dir: Path,
    model: str,
    overwrite: bool,
    stats: RunStats,
) -> None:
    out = match.output_path(output_dir, doc_id, action.action_id)
    if out.exists() and not overwrite:
        stats.add_skip()
        return

    last_err: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            payload = match.match_pair(
                action=action,
                doc_id=doc_id,
                doc_meta=doc_meta,
                atoms_dir=atoms_dir,
                model=model,
            )
            break
        except Exception as exc:
            last_err = exc
            err_name = type(exc).__name__
            retryable = "RateLimit" in err_name or "Timeout" in err_name or "APIConnection" in err_name
            if not retryable or attempt == MAX_RETRIES - 1:
                raise
            time.sleep(min(60, 2 ** attempt))
    else:
        raise last_err or RuntimeError("match_pair failed")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    run = payload.get("search_run") or {}
    stats.add_ok(
        inp=int(run.get("input_tokens") or 0),
        cached=int(run.get("cached_input_tokens") or 0),
        out=int(run.get("output_tokens") or 0),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="v2 batch atom-matching runner")
    ap.add_argument("--actions", type=Path, default=ef.DEFAULT_ACTIONS_JSON,
                    help="Path to actions.json (or legacy actions_profiled.csv).")
    ap.add_argument("--registry", type=Path, default=ef.DEFAULT_REGISTRY)
    ap.add_argument("--atoms-dir", type=Path, default=DEFAULT_ATOMS_DIR)
    ap.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    ap.add_argument("--action", help="single action_id")
    ap.add_argument("--doc", help="single source_document_id")
    ap.add_argument("--all-actions", action="store_true")
    ap.add_argument("--all-docs", action="store_true")
    ap.add_argument("--model", default=match.DEFAULT_MODEL)
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--dry-list", action="store_true")
    args = ap.parse_args()

    actions = ef.load_actions(args.actions)
    registry = ef.load_registry(args.registry)
    doc_ids = list_doc_ids_with_atoms(args.atoms_dir, registry)
    pairs = build_pairs(
        actions, doc_ids,
        args.action, args.doc, args.all_actions, args.all_docs,
    )

    if args.dry_list:
        print(f"pairs={len(pairs)} actions={len(actions)} docs_with_atoms={len(doc_ids)}")
        for action, doc_id in pairs[:10]:
            print(f"  {action.action_id} x {doc_id}")
        if len(pairs) > 10:
            print(f"  ... and {len(pairs) - 10} more")
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    failed_log = args.output_dir / "failed.jsonl"
    stats = RunStats()
    started = time.time()
    total = len(pairs)

    print(
        f"starting {total} pairs model={args.model} concurrency={args.concurrency}",
        file=sys.stderr,
        flush=True,
    )

    def run_one(pair: tuple[ef.Action, str]) -> None:
        action, doc_id = pair
        doc_meta = dict(registry[doc_id])
        doc_meta["source_document_id"] = doc_id
        try:
            process_pair(
                action, doc_id, doc_meta,
                args.atoms_dir, args.output_dir,
                args.model, args.overwrite, stats,
            )
        except Exception as exc:
            stats.add_fail()
            with stats.lock:
                with failed_log.open("a", encoding="utf-8") as f:
                    f.write(
                        json.dumps(
                            {
                                "action_id": action.action_id,
                                "source_document_id": doc_id,
                                "error": f"{type(exc).__name__}: {exc}",
                                "at": datetime.now(timezone.utc).isoformat(),
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
            print(
                f"FAIL {action.action_id} x {doc_id}: {exc}",
                file=sys.stderr,
                flush=True,
            )

    completed = 0
    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [pool.submit(run_one, p) for p in pairs]
        for fut in as_completed(futures):
            fut.result()
            completed += 1
            if completed % STATUS_EVERY == 0 or completed == total:
                print_status(stats, total, started)

    print_status(stats, total, started)
    return 0 if stats.fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
