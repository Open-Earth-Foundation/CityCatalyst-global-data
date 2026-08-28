---
name: script-quality-gate
description: Apply when adding or modifying runnable scripts (cc-mage/local_scripts/*, helpers, CLI tools).
---

# script-quality-gate — global-data

Use when creating or changing a runnable script (anything with `if __name__ == "__main__"`).

## Required

- Top-level docstring (Brief / Inputs / Outputs / Usage).
- `argparse` for CLIs, `--help` reachable.
- Work inside `def main()`. No side effects at import time.
- `pathlib.Path` for paths.
- `logging` for production-meaningful output.
- Absolute imports.

## Location

- One-off / exploratory: `cc-mage/local_scripts/<name>.py` (NOT shipped in production image).
- Shared helpers: `cc-mage/utils/<module>.py`.
- Standalone tools: top-level `scripts/<name>.py` (only if no Mage block fits).

## After the checklist

Run the `docs-after-change` skill.
