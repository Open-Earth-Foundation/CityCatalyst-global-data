"""
Repair character-encoding mojibake in CSV files.

Two failure modes are handled:

1.  **Known-value fixes.** A small set of templated values in
    ``climate_classification_es`` are *truncated mid-character* in the upstream
    export — the original UTF-8 byte for ``ó`` got chopped, so a plain
    ``latin-1 -> utf-8`` round-trip raises ``UnicodeDecodeError``. These need
    an explicit lookup table, populated from observed corruption patterns.

2.  **Generic round-trip.** Most other mojibake (intact strings where the
    bytes survived a wrong-encoding round-trip) can be repaired by
    ``value.encode("latin-1").decode("utf-8")``. The script applies this only
    when the result no longer contains the tell-tale ``Ã`` character.

Cells that cannot be repaired by either path are left unchanged and logged.

Usage
-----
    python scripts/fix_mojibake.py path/to/file.csv --in-place
    python scripts/fix_mojibake.py path/to/file.csv -o out.csv
    python scripts/fix_mojibake.py path/to/file.csv --dry-run
    python scripts/fix_mojibake.py path/to/file.csv --columns nombre,climate_classification_es
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Known-value fixes: truncated templated values that can't be round-tripped.
# ---------------------------------------------------------------------------

KNOWN_VALUE_FIXES: dict[str, str] = {
    "Proyecto de movilidad activa con contribuciÃ³n climÃ¡tica explÃ":
        "Proyecto de movilidad activa con contribución climática explícita.",
    "Proyecto con contribuciÃ³n climÃ¡tica explÃ":
        "Proyecto con contribución climática explícita.",
    "Proyecto con componente explÃ":
        "Proyecto con componente explícito.",
}


# ---------------------------------------------------------------------------
# Repair logic
# ---------------------------------------------------------------------------

def repair_cell(value: str) -> tuple[str, str | None]:
    """Return (fixed_value, repair_kind_or_None).

    ``repair_kind`` is one of ``"known_value_fix"``, ``"roundtrip"``,
    ``"unfixable"``, or ``None`` if the cell didn't need repair.
    """
    if not value or "Ã" not in value:
        return value, None
    if value in KNOWN_VALUE_FIXES:
        return KNOWN_VALUE_FIXES[value], "known_value_fix"
    try:
        candidate = value.encode("latin-1").decode("utf-8")
    except UnicodeError:
        return value, "unfixable"
    if "Ã" in candidate:
        return value, "unfixable"
    return candidate, "roundtrip"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path, help="Input CSV path.")
    ap.add_argument("-o", "--output", type=Path, default=None,
                    help="Output CSV path. If omitted (and --in-place not set), prints to stdout.")
    ap.add_argument("--in-place", action="store_true",
                    help="Overwrite input; writes a .bak copy next to it first.")
    ap.add_argument("--columns", default=None,
                    help="Comma-separated columns to scan. Default: all columns.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Report counts; don't write any output.")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"error: input not found: {args.input}", file=sys.stderr)
        return 1
    if args.in_place and args.output is not None:
        print("error: --in-place and --output are mutually exclusive", file=sys.stderr)
        return 2

    target_cols: set[str] | None
    if args.columns:
        target_cols = {c.strip() for c in args.columns.split(",") if c.strip()}
    else:
        target_cols = None

    # Read everything.
    with open(args.input, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    scan_cols = [c for c in fieldnames if (target_cols is None or c in target_cols)]

    counts = {"known_value_fix": 0, "roundtrip": 0, "unfixable": 0}
    affected_columns: dict[str, int] = {}
    unfixable_log: list[tuple[int, str, str]] = []

    for i, row in enumerate(rows):
        for c in scan_cols:
            fixed, kind = repair_cell(row.get(c) or "")
            if kind is None:
                continue
            if kind == "unfixable":
                unfixable_log.append((i, c, (row.get(c) or "")[:80]))
            else:
                row[c] = fixed
            counts[kind] += 1
            affected_columns[c] = affected_columns.get(c, 0) + (1 if kind != "unfixable" else 0)

    total_fixed = counts["known_value_fix"] + counts["roundtrip"]
    print(f"Scanned {len(rows)} rows across {len(scan_cols)} column(s).")
    print(f"Fixed {total_fixed} cells "
          f"(known_value_fix={counts['known_value_fix']}, "
          f"roundtrip={counts['roundtrip']}, "
          f"unfixable={counts['unfixable']}).")
    if affected_columns:
        print("By column:")
        for c, n in sorted(affected_columns.items(), key=lambda x: -x[1]):
            print(f"  {c}: {n}")
    for i, c, preview in unfixable_log:
        print(f"[unfixable] {args.input}:row {i} col {c}: {preview!r}", file=sys.stderr)

    if args.dry_run:
        print("(dry-run; no output written)")
        return 0

    # Determine output path.
    if args.in_place:
        bak = args.input.with_suffix(args.input.suffix + ".bak")
        shutil.copy2(args.input, bak)
        print(f"backup: {bak}")
        out_path = args.input
    elif args.output is not None:
        out_path = args.output
    else:
        out_path = None  # stdout

    handle = open(out_path, "w", encoding="utf-8-sig", newline="") if out_path else sys.stdout
    try:
        w = csv.DictWriter(handle, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    finally:
        if out_path is not None:
            handle.close()
    if out_path is not None:
        print(f"wrote: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
