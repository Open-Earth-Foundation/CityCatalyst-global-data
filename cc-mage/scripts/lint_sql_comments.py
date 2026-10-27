#!/usr/bin/env python3
"""Fail if any SQL `--` comment contains a character that breaks Mage's query splitter.

Mage pre-processes raw-SQL blocks by tracking quote/statement state — through `--` comments
too. So an apostrophe, double-quote, or semicolon inside a comment makes a block fail
(`syntax error at end of input`, or a fragment after a `;` runs as its own statement).

Usage:
    python lint_sql_comments.py file1.sql file2.sql ...   # pre-commit passes changed files
    python lint_sql_comments.py path/to/dir                # scan a directory recursively
"""
import os
import sys

HAZARDS = ("'", '"', ";")


def hazards_in(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            i = line.find("--")
            if i == -1:
                continue
            comment = line[i + 2:]
            hits = [c for c in HAZARDS if c in comment]
            if hits:
                out.append((n, "".join(hits), line.strip()))
    return out


def expand(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for fn in files:
                    if fn.endswith(".sql"):
                        yield os.path.join(root, fn)
        elif p.endswith(".sql"):
            yield p


def main(argv):
    failures = 0
    for path in expand(argv):
        for ln, chars, text in hazards_in(path):
            failures += 1
            print(f"{path}:{ln}: SQL comment contains {chars!r} (breaks Mage's splitter): {text}")
    if failures:
        print(f"\n{failures} SQL-comment hazard(s). Keep `--` comments plain ASCII: "
              f"no apostrophes, double-quotes, or semicolons (write `dataset` not `dataset's`).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
