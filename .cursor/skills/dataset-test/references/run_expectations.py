#!/usr/bin/env python3
"""Post-load data validation + profiling for a modelled.* table.

Reads an expectations.yaml, checks the live table in the global-api DB, and writes a
validation_report.md (the "what we can say about this data" statement). Exits non-zero
if any hard check fails — so it doubles as a gate.

Usage:
    python run_expectations.py path/to/expectations.yaml [--report path/to/report.md] [--dry-run]

DB connection (read locally; never committed):
    DATABASE_URL=postgresql://user:pass@host:port/dbname     (preferred)
  or DB_NAME / DB_USER / DB_PASSWORD / DB_HOST / DB_PORT      (as global-api/.env)

Design notes:
  - Three check tiers map onto the data-quality layers:
      structural  — the contract (PK, not-null, unique, FK): hard fail
      invariants  — what's true in reality across any release (value sets, ranges,
                    row rules): hard fail
      snapshot    — this release's observed facts (counts, distributions): regression
  - profile is descriptive (null rates, value distributions, ranges) — it never fails;
    it's the statement about the data, and the source for writing the snapshot block.
"""
import argparse
import os
import sys

import yaml

# ----------------------------------------------------------------------------- DB
class DB:
    """Thin wrapper; in --dry-run it records SQL and returns benign stubs."""

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.sql_log = []
        self.conn = None
        if not dry_run:
            import psycopg2  # imported lazily so --dry-run needs no driver/DB
            url = os.environ.get("DATABASE_URL")
            if url:
                self.conn = psycopg2.connect(url)
            else:
                self.conn = psycopg2.connect(
                    dbname=os.environ["DB_NAME"], user=os.environ["DB_USER"],
                    password=os.environ.get("DB_PASSWORD", ""),
                    host=os.environ.get("DB_HOST", "localhost"),
                    port=os.environ.get("DB_PORT", "5432"),
                )

    def scalar(self, sql, args=None):
        self.sql_log.append(sql)
        if self.dry_run:
            return 0
        with self.conn.cursor() as cur:
            cur.execute(sql, args or ())
            return cur.fetchone()[0]

    def rows(self, sql, args=None):
        self.sql_log.append(sql)
        if self.dry_run:
            return []
        with self.conn.cursor() as cur:
            cur.execute(sql, args or ())
            return cur.fetchall()


# ------------------------------------------------------------------------- checks
def _result(name, level, passed, detail):
    return {"name": name, "level": level, "passed": passed, "detail": detail}


def check_structural(db, table, spec):
    out = []
    pk = spec.get("primary_key")
    if pk:
        dups = db.scalar(f"SELECT count(*) FROM (SELECT 1 FROM {table} GROUP BY {pk} HAVING count(*) > 1) d")
        nulls = db.scalar(f"SELECT count(*) FROM {table} WHERE {pk} IS NULL")
        out.append(_result(f"pk {pk} unique & not-null", "fail", dups == 0 and nulls == 0,
                           f"{dups} duplicate keys, {nulls} null keys"))
    for col in spec.get("required_not_null", []):
        n = db.scalar(f"SELECT count(*) FROM {table} WHERE {col} IS NULL")
        out.append(_result(f"{col} not null", "fail", n == 0, f"{n} nulls"))
    for key in spec.get("unique", []):
        cols = ", ".join(key)
        dups = db.scalar(f"SELECT count(*) FROM (SELECT 1 FROM {table} GROUP BY {cols} HAVING count(*) > 1) d")
        out.append(_result(f"unique ({cols})", "fail", dups == 0, f"{dups} duplicate groups"))
    for fk in spec.get("foreign_keys", []):
        col, ref = fk["column"], fk["references"]
        ref_table, ref_col = ref.rsplit(".", 1)
        n = db.scalar(f"SELECT count(*) FROM {table} t WHERE t.{col} IS NOT NULL "
                      f"AND NOT EXISTS (SELECT 1 FROM {ref_table} r WHERE r.{ref_col} = t.{col})")
        out.append(_result(f"fk {col} -> {ref}", "fail", n == 0, f"{n} orphan rows"))
    return out


def check_value_sets(db, table, value_sets, level):
    out = []
    for col, allowed in value_sets.items():
        n = db.scalar(f"SELECT count(*) FROM {table} WHERE {col} IS NOT NULL AND NOT ({col} = ANY(%s))",
                      [list(allowed)])
        bad = db.rows(f"SELECT DISTINCT {col} FROM {table} WHERE {col} IS NOT NULL AND NOT ({col} = ANY(%s))",
                      [list(allowed)])
        out.append(_result(f"{col} in allowed set", level, n == 0,
                           f"{n} rows with unexpected value(s): {[r[0] for r in bad][:10]}"))
    return out


def check_invariants(db, table, spec):
    out = check_value_sets(db, table, spec.get("value_sets", {}), "fail")
    for col, rng in spec.get("ranges", {}).items():
        lo, hi = rng.get("min"), rng.get("max")
        conds = []
        if lo is not None:
            conds.append(f"{col} < {lo}")
        if hi is not None:
            conds.append(f"{col} > {hi}")
        cond = " OR ".join(conds)
        n = db.scalar(f"SELECT count(*) FROM {table} WHERE {col} IS NOT NULL AND ({cond})")
        out.append(_result(f"{col} in range [{lo}, {hi}]", "fail", n == 0, f"{n} out-of-range rows"))
    for rule in spec.get("row_rules", []):
        # a row passes when the expression is true or null; fails only when explicitly FALSE
        n = db.scalar(f"SELECT count(*) FROM {table} WHERE ({rule}) IS FALSE")
        out.append(_result(f"row rule: {rule}", "fail", n == 0, f"{n} violating rows"))
    return out


def check_snapshot(db, table, spec):
    out = []
    rc = spec.get("row_count")
    if rc:
        total = db.scalar(f"SELECT count(*) FROM {table}")
        if "equals" in rc:
            out.append(_result("row_count", "fail", total == rc["equals"], f"{total} (expected {rc['equals']})"))
        else:
            ok = (rc.get("min", total) <= total <= rc.get("max", total))
            out.append(_result("row_count in range", "fail", ok, f"{total} (expected {rc})"))
    for col, n_exp in spec.get("distinct_count", {}).items():
        n = db.scalar(f"SELECT count(DISTINCT {col}) FROM {table}")
        out.append(_result(f"distinct {col}", "fail", n == n_exp, f"{n} (expected {n_exp})"))
    for col, expected in spec.get("group_counts", {}).items():
        got = dict(db.rows(f"SELECT {col}, count(*) FROM {table} GROUP BY {col}"))
        ok = all(got.get(k) == v for k, v in expected.items())
        out.append(_result(f"group_counts {col}", "fail", ok, f"got {got} (expected {expected})"))
    for col, n_min in spec.get("min_non_null", {}).items():
        n = db.scalar(f"SELECT count({col}) FROM {table}")
        out.append(_result(f"{col} non-null >= {n_min}", "fail", n >= n_min, f"{n} non-null"))
    return out


# ------------------------------------------------------------------------ profile
def build_profile(db, table, spec):
    p = {}
    p["total_rows"] = db.scalar(f"SELECT count(*) FROM {table}")
    p["nulls"] = db.rows(
        f"SELECT key, count(*) FILTER (WHERE value IS NULL) AS nulls, count(*) AS total "
        f"FROM {table} t, LATERAL jsonb_each_text(to_jsonb(t)) j(key, value) "
        f"GROUP BY key HAVING count(*) FILTER (WHERE value IS NULL) > 0 ORDER BY nulls DESC")
    part = spec.get("partition_by")
    p["partition"] = db.rows(f"SELECT {part}, count(*) FROM {table} GROUP BY 1 ORDER BY 2 DESC") if part else []
    prof = spec.get("profile", {})
    p["categorical"] = {c: db.rows(f"SELECT {c}, count(*) FROM {table} GROUP BY 1 ORDER BY 2 DESC")
                        for c in prof.get("categorical", [])}
    p["numeric"] = {c: db.rows(f"SELECT min({c}), max({c}), round(avg({c}),1), count({c}) FROM {table}")
                    for c in prof.get("numeric", [])}
    p["dates"] = {c: db.rows(f"SELECT min({c}), max({c}), count({c}) FROM {table}")
                  for c in prof.get("dates", [])}
    return p


# ------------------------------------------------------------------------- report
def render_report(table, results, profile):
    failed = [r for r in results if r["level"] == "fail" and not r["passed"]]
    L = [f"# Validation report — `{table}`", ""]
    L.append(f"**{'PASS' if not failed else 'FAIL'}** — {len(results) - len(failed)}/{len(results)} checks passed, "
             f"{len(failed)} hard failure(s). {profile['total_rows']} rows.\n")

    L.append("## Checks\n")
    for r in results:
        mark = "✅" if r["passed"] else ("❌" if r["level"] == "fail" else "⚠️")
        L.append(f"- {mark} **{r['name']}** — {r['detail']}")
    L.append("")

    L.append("## What we can say about this data\n")
    if profile["partition"]:
        L.append("**By source:** " + ", ".join(f"{k} {v}" for k, v in profile["partition"]) + "\n")
    if profile["nulls"]:
        L.append("**Columns with nulls:**\n")
        for key, nulls, total in profile["nulls"]:
            L.append(f"- `{key}`: {nulls}/{total} null ({round(100*nulls/total)}%)")
        L.append("")
    else:
        L.append("**No nulls in any column.**\n")
    for col, vals in profile["categorical"].items():
        L.append(f"**`{col}` values:** " + ", ".join(f"{v} ({n})" for v, n in vals))
    if profile["categorical"]:
        L.append("")
    for col, (row,) in profile["numeric"].items():
        L.append(f"**`{col}`:** min {row[0]}, max {row[1]}, avg {row[2]}, non-null {row[3]}")
    for col, (row,) in profile["dates"].items():
        L.append(f"**`{col}`:** {row[0]} → {row[1]} ({row[2]} non-null)")
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("expectations")
    ap.add_argument("--report", default=None, help="output path (default: report.md next to expectations)")
    ap.add_argument("--dry-run", action="store_true", help="print the SQL it would run; no DB needed")
    args = ap.parse_args()

    spec = yaml.safe_load(open(args.expectations))
    table = spec["table"]
    db = DB(dry_run=args.dry_run)

    results = []
    results += check_structural(db, table, spec.get("structural", {}))
    results += check_invariants(db, table, spec.get("invariants", {}))
    results += check_snapshot(db, table, spec.get("snapshot", {}))

    if args.dry_run:
        print(f"-- {len(db.sql_log)} queries for {table}\n")
        print("\n".join(s + ";" for s in db.sql_log))
        return 0

    profile = build_profile(db, table, spec)
    report = render_report(table, results, profile)
    report_path = args.report or os.path.join(os.path.dirname(args.expectations) or ".", "validation_report.md")
    with open(report_path, "w") as f:
        f.write(report)

    failed = [r for r in results if r["level"] == "fail" and not r["passed"]]
    print(report)
    print(f"\nReport written to {report_path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
