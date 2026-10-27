#!/usr/bin/env python3
"""Check that every opportunity points to a real, reachable webpage.

Reads distinct source_url values from a modelled table and does a lightweight HEAD (falling
back to GET) on each, reporting status. Flags:
  - rows with NO source_url (the gap to explain — which source, why)
  - URLs that do not resolve (4xx/5xx/timeout) — a dead or moved page

Run it locally (it needs network + the DB):
    DATABASE_URL=postgresql://user:pass@host:port/db \
      python check_source_urls.py modelled.finance_opportunity [--column source_url]

Network-dependent and slow, so this is a manual/periodic check, not a pre-commit gate.
"""
import argparse
import os
import sys

import requests


def get_conn():
    import psycopg2
    url = os.environ.get("DATABASE_URL")
    if url:
        return psycopg2.connect(url)
    return psycopg2.connect(
        dbname=os.environ["DB_NAME"], user=os.environ["DB_USER"],
        password=os.environ.get("DB_PASSWORD", ""),
        host=os.environ.get("DB_HOST", "localhost"), port=os.environ.get("DB_PORT", "5432"),
    )


def status_of(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=15)
        if r.status_code >= 400:                 # some servers reject HEAD; retry GET
            r = requests.get(url, allow_redirects=True, timeout=20, stream=True)
        return r.status_code
    except requests.RequestException as e:
        return f"ERROR {type(e).__name__}"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("table")
    ap.add_argument("--column", default="source_url")
    ap.add_argument("--id-column", default="source_dataset", help="grouping for the missing-url report")
    args = ap.parse_args()
    col, table = args.column, args.table

    with get_conn() as conn, conn.cursor() as cur:
        # which rows have no URL, by source
        cur.execute(f"SELECT {args.id_column}, count(*) FROM {table} WHERE {col} IS NULL GROUP BY 1 ORDER BY 2 DESC")
        missing = cur.fetchall()
        # distinct URLs to test
        cur.execute(f"SELECT {col}, count(*) FROM {table} WHERE {col} IS NOT NULL GROUP BY 1 ORDER BY 2 DESC")
        urls = cur.fetchall()

    total_missing = sum(n for _, n in missing)
    print(f"== source_url liveness for {table} ==\n")
    if missing:
        print(f"MISSING a {col} ({total_missing} rows) — investigate why these have no page:")
        for src, n in missing:
            print(f"  - {src}: {n}")
        print()
    else:
        print(f"Every row has a {col}.\n")

    bad = []
    print(f"Checking {len(urls)} distinct URLs ...")
    for url, n in urls:
        st = status_of(url)
        ok = isinstance(st, int) and st < 400
        if not ok:
            bad.append((url, st, n))
        print(f"  [{st}] x{n}  {url}")

    print()
    if bad:
        print(f"{len(bad)} URL(s) did not resolve cleanly:")
        for url, st, n in bad:
            print(f"  [{st}] x{n}  {url}")
    print(f"\nSummary: {len(urls)-len(bad)}/{len(urls)} URLs live, {len(bad)} dead, {total_missing} rows missing a URL.")
    return 1 if (bad or total_missing) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
