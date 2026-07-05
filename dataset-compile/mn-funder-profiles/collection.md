# mn-funder-profiles — collection notes

Structured funder profiles for the Concept Note Builder. A **staging** dataset in the compile family, but a different shape from `mn-climate-awards`: one nested profile document per funder (`profiles/<slug>.yaml`), not one row per record. See `schema.json` for the object shape.

## What a funder profile is (and does)

The awards KB answers "what does a funded project look like?"; a funder profile answers "what does *this funder* require?" It's the target a concept note is written toward, and it does three jobs: (1) structures the guided interview, (2) drives matching toward the funder's gates, (3) shapes the output to the funder's template. It defines the "100" in the 70→100 fundability framing.

## The two-halves design

Each profile is assembled from two sources, tagged per section:

- **stated** — read from the funder's own RFP / program docs. Authoritative, sourced, status-flagged.
- **derived** — computed from `dataset-compile/mn-climate-awards` (the "revealed" half: who actually wins, typical sizes, applicant types, category & region split).

The two datasets join on **funder + route**. Building the awards KB first is what lets the revealed half be populated immediately.

## Profiles in this dataset

- `bwsr-clean-water-fund.yaml` — **BWSR Clean Water Fund, Projects & Practices** (Route A grant). Prototype. Stated half transcribed from the FY27 P&P RFP (eligibility, ≥10% match, the 100-point scoring rubric, the eLINK application question set, required attachments, timeline). Revealed half computed from our 18 FY27 BWSR award rows (median $289,500; winners mostly watershed districts/SWCDs; cities a minority — Hibbing, Vadnais Heights).

## How it was built

1. Computed the revealed half from `mn-climate-awards` (BWSR CWF rows).
2. Pulled the stated half from the FY27 RFP PDF (`pdftotext` locally; the scoring rubric is the application questions with point weights — they sum to 100).
3. Structured into the profile object, tagging every section stated / derived / meta.

## Verification status

- **Rubric** — the P&P criteria point weights read from the RFP sum to exactly 100 (5+15+2+20+5+25+5+13+5+2+3). High confidence.
- **Eligibility, match, timeline** — read directly from the FY27 RFP.
- **Revealed half** — computed from the awards dataset (itself verified against BWSR's published subtotals).

## Known gaps / to-proper

- **Drinking Water variant rubric** — captured only its top weights; the full DW question set/points aren't transcribed.
- **NLC co-calibration** — the rubric is transcribed from the RFP, but per the PRD the matching emphasis/thresholds must be confirmed with NLC before the CNB scores against it. Not done.
- **eLINK exact field labels / char mechanics** — question *intent* captured; exact eLINK field names and per-field limits should be confirmed against the live application before using as the output template.
- **Annual refresh** — the RFP is annual; re-verify each fiscal year (see sources.yaml).
- **Second funder** — only BWSR CWF built; the schema is meant to generalize (SRF/PFA, Met Council, DNR are the next candidates).

## Refresh model

No feed. Refresh = re-pull the funder's current RFP (sources.yaml) and re-run the revealed half against the latest awards. `last_verified` lives in each profile's `provenance` block.

## Promotion

Graduates into `dataset-review` when stated fields are re-verified against the live NOFO, the rubric is confirmed with NLC, and the schema is locked — then it feeds the CNB funder-profile service.
