#!/usr/bin/env python3
"""Check that every row in a cleaned dataset has a real, reachable `source_url`.

Enforces the data-integrity invariant from the pipeline rules: every opportunity must link to an
actual page a user can open (never null), and that page must resolve. Two checks:

  1) null/empty       — any blank `source_url` is a failure (fix in the extract or record why in
                        the review; do NOT backfill to a generic landing page).
  2) liveness         — HEAD each distinct URL (falling back to GET), flag anything that is not
                        reachable / returns a 4xx-5xx. Skipped with --no-network for offline runs.

Stdlib only (urllib) so it runs anywhere without extra deps.

Usage:
    python check_source_urls.py opportunities.csv               # null check + liveness
    python check_source_urls.py data/ --column source_url       # scan a directory of CSVs
    python check_source_urls.py opportunities.csv --no-network   # null check only (fast/offline)
    python check_source_urls.py opportunities.csv --allow-null   # do not fail on blank URLs
"""
import argparse
import csv
import os
import sys
import urllib.error
import urllib.request

DEFAULT_COLUMN = "source_url"
DEFAULT_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (compatible; CityCatalyst-source-url-check/1.0)"


def expand(paths):
    """Yield every .csv under the given files/dirs."""
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for fn in files:
                    if fn.endswith(".csv"):
                        yield os.path.join(root, fn)
        elif p.endswith(".csv"):
            yield p


def read_urls(path, column):
    """Return (rows_total, blank_row_numbers, distinct_urls) for one CSV.

    Raises KeyError-style ValueError if the column is absent so a typo fails loudly.
    """
    blanks = []
    urls = set()
    total = 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if column not in (reader.fieldnames or []):
            raise ValueError(f"{path}: no '{column}' column (found {reader.fieldnames})")
        for n, row in enumerate(reader, 2):  # row 1 is the header
            total += 1
            value = (row.get(column) or "").strip()
            if not value:
                blanks.append(n)
            else:
                urls.add(value)
    return total, blanks, urls


def is_reachable(url, timeout):
    """HEAD the URL, falling back to GET. Return (ok, detail)."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return True, f"{resp.status}"
        except urllib.error.HTTPError as e:
            # Some servers reject HEAD with 403/405 but serve GET — let the loop retry once.
            if method == "HEAD" and e.code in (403, 405):
                continue
            return False, f"HTTP {e.code}"
        except (urllib.error.URLError, ValueError, OSError) as e:
            if method == "HEAD":
                continue
            return False, str(getattr(e, "reason", e))
    return False, "unreachable"


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", help="CSV file(s) or directory(ies) to check")
    parser.add_argument("--column", default=DEFAULT_COLUMN, help=f"URL column name (default: {DEFAULT_COLUMN})")
    parser.add_argument("--no-network", action="store_true", help="skip the liveness check (null check only)")
    parser.add_argument("--allow-null", action="store_true", help="do not fail on blank source_url")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"per-request timeout s (default: {DEFAULT_TIMEOUT})")
    args = parser.parse_args(argv)

    files = sorted(set(expand(args.paths)))
    if not files:
        print("No .csv files found in the given paths.")
        return 1

    failures = 0
    all_urls = set()

    # Per-file structural check: the column exists and no row is blank.
    for path in files:
        try:
            total, blanks, urls = read_urls(path, args.column)
        except ValueError as e:
            print(e)
            failures += 1
            continue
        all_urls |= urls
        print(f"{path}: {total} rows, {len(urls)} distinct {args.column}, {len(blanks)} blank")
        if blanks and not args.allow_null:
            failures += len(blanks)
            preview = ", ".join(str(b) for b in blanks[:10]) + ("…" if len(blanks) > 10 else "")
            print(f"  blank {args.column} on row(s): {preview} (capture the real per-row URL or record why in the review)")

    # Cross-file liveness check on the union of distinct URLs.
    if not args.no_network and all_urls:
        print(f"\nChecking liveness of {len(all_urls)} distinct URL(s)…")
        for url in sorted(all_urls):
            ok, detail = is_reachable(url, args.timeout)
            if not ok:
                failures += 1
                print(f"  DEAD ({detail}): {url}")

    if failures:
        print(f"\n{failures} source_url issue(s). Every row needs a real, reachable source_url.")
        return 1
    print("\nAll source_url values present and reachable.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
