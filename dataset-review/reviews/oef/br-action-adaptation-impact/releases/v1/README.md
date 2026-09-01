# V1 implementation

V1 has one assessment runner and one generated delivery. Intermediate PDF text and
model checkpoints are disposable cache files rather than additional datasets.

```text
v1/
├── README.md
├── input/
│   ├── actions.csv
│   ├── risk_framework.csv
│   ├── sources.csv
│   └── documents/*.pdf
├── prompts/
│   ├── eligibility.md
│   └── evidence.md
├── run.py
├── output/
│   ├── action_risk_assessments.json
│   └── 07_icare_adaptation_assessment_review_strict.xlsx
├── .cache/
│   ├── extracted_text/
│   └── model_responses/
└── archive/
    ├── historical Excel files
    └── legacy_pipeline/     # ignored local backup of the superseded implementation
```

## What is authoritative

- `input/` contains the source facts used by the assessment.
- `prompts/` contains the two versioned AI instructions.
- `run.py` contains extraction, model calls, validation, quote grounding and component
  claim derivation.
- `output/action_risk_assessments.json` is the only assessment dataset.
- The Excel file in `output/` is a human-review view generated from that JSON.
- `.cache/` is ignored by Git and can be deleted and rebuilt.
- `archive/` preserves the original workbooks. Its ignored `legacy_pipeline/` folder is
  a local, recoverable backup of the superseded implementation. Nothing in the archive
  is read by `run.py`.

The source registry has one row per document. Its `sectors` field lists every sector in
which the document is searched, avoiding duplicate source metadata.

## JSON structure

The JSON contains the risk framework and source registry once. Each action then has:

- `indicator_claims` — direct, indirect or unclear indicator relationships; when
  screening is complete, omitted indicators are `no_link`;
- `source_screening` — sources checked for an action, sector, risk and component;
- `evidence` — page-located quotes tied to one action, sector, risk and component;
- `component_claims` — effectiveness for an action, sector, risk and component,
  referencing evidence by ID.

## Run

Validate the current JSON without an API call:

```bash
python3 run.py validate
```

After changing `input/sources.csv` or adding PDFs, refresh the source registry in the
existing JSON without rerunning any model assessment:

```bash
python3 run.py sync-sources
```

This marks the delivery as pending an evidence rerun. It does not imply that newly
added sources have already been screened.

Preview the number of model calls:

```bash
python3 run.py eligibility --dry-run
python3 run.py evidence --dry-run
```

Run the stages with `OPENAI_API_KEY` set:

```bash
python3 run.py eligibility
python3 run.py evidence
```

Or rebuild both stages:

```bash
python3 run.py all
```

Model responses are checkpointed under `.cache/model_responses/`, so an interrupted run
can reuse completed calls. Pass `--force` only when those responses should be replaced.

The evidence stage uses Poppler's `pdfinfo` and `pdftotext` commands. It extracts PDF
text into `.cache/extracted_text/`, retrieves candidate pages using the action and exact
sector-risk context, validates structured model output and grounds every quote against
its cited page. Prompt version 1.2.0 requires the quote to demonstrate the action,
sector, risk, component and at least one named direct indicator. It also captures an
outcome-strength signal used to derive High, Medium, Low or No demonstrated
effectiveness without treating scientific confidence as effect magnitude.

## Current status

The source registry now includes five locally verified IPCC chapter PDFs covering cities,
health, livelihoods, Central and South America, and adaptation decision-making. It also
contains six locally verified 2025 Brazilian Plano Clima PDFs for biodiversity, energy,
water resources, disaster risk, health, and food security. The official GOV.BR URLs are
retained as canonical provenance; because those URLs currently redirect to restricted
content, the exact PDF bytes were recovered from the Climate Policy Radar mirrors already
documented by the Brazil federal climate-policy review.

The strict evidence refresh was completed on 2026-09-01 without an external model call.
All eleven added PDFs were screened for every applicable action × sector × risk ×
component group. The current assessment contains 53 actions, 456 direct indicator claims,
363 indirect claims, 232 component assessments, 3,073 source-screening records and 140
retained evidence records. Every added quote was checked against its cited local PDF page.

The six Brazilian plans are included in source screening, but policy targets and intended
effects were not treated as demonstrated effectiveness. The JSON now uses only High,
Medium, Low and No demonstrated effectiveness. A normal reproducible rerun still uses
`python3 run.py evidence`, the versioned prompt and the source PDFs described above.
