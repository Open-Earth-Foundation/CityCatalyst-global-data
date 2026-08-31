"""Run the six numbered stages in order."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(script: str, *arguments: str) -> None:
    print(f"\n== {script} ==", flush=True)
    subprocess.run(
        [sys.executable, "-B", str(HERE / script), *arguments],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mapping-input",
        default=str(ROOT / "data" / "input" / "mapping_proposals.csv"),
    )
    parser.add_argument(
        "--evidence-input",
        default=str(ROOT / "data" / "input" / "evidence_proposals.csv"),
    )
    parser.add_argument("--match-run-id", default="all_sector_mapping")
    parser.add_argument("--skip-document-extraction", action="store_true")
    args = parser.parse_args()

    run("01_prepare_inputs.py")
    if not args.skip_document_extraction:
        run("02_extract_documents.py")
    run(
        "03_match_actions.py",
        "--input", args.mapping_input,
        "--run-id", args.match_run_id,
    )
    run("04_extract_evidence.py", "--input", args.evidence_input)
    run("05_verify_evidence_grounding.py")
    run("06_build_warehouse_output.py")


if __name__ == "__main__":
    main()
