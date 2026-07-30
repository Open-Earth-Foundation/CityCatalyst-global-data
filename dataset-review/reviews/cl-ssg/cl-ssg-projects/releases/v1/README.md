# cl-ssg-projects v1

Pipeline assets for parsing Chile SNI/BIP FICHA PDFs, flattening to tabular data, enriching with English narrative, and matching projects to climate actions.

## Layout

- `scripts/`: runnable pipeline scripts in execution order.
- `data/inputs/`: static and external inputs — `actions.csv`, `gpc_mapping_v1.csv`, externally sourced `projects.csv` and `projects_finance.csv`, and optional external `bip_database.csv` (not tracked in repo).
- `data/derived/`: generated tables and caches (`ficha_idi_table.csv`, `ficha_idi_table_translated.csv`, `translations_es_en.json`, `project_action_matches.csv`, `actions_profiled.csv`, optional `projects_rebuilt.csv` from the rebuild utility).
- `data/qa/`: QA samples and review files.
- `corpus/pdfs/`: raw source PDFs by sector.
- `corpus/parsed/`: parsed JSON corpus generated from PDFs.
- `corpus/parsed_subset/`: optional smaller parsed subset for quick testing.

## Pipeline

1. `python scripts/01_parse_pdfs.py ...`
2. `python scripts/02_flatten_to_table.py`
3. `python scripts/03_add_english_columns.py` — writes `data/derived/ficha_idi_table_translated.csv` (bilingual ES + EN; use `--translations-cache` with `data/derived/translations_es_en.json` after step 4 when rebuilding).
4. `python scripts/04_translate_narrative.py`
5. `python scripts/05_build_projects_table.py` — optional rebuild from `bip_database.csv` → `data/derived/projects_rebuilt.csv`; canonical `projects.csv` is external under `data/inputs/`.
6. `python scripts/06_match_to_actions.py`
7. `python scripts/07_export_finance_project_inputs.py` — builds and validates the two files for the Mage finance-project pipeline.

## Key data files

- **`data/inputs/actions.csv`** — action library for matching.
- **`data/inputs/gpc_mapping_v1.csv`** — sector/subsector → GPC mapping.
- **`data/inputs/projects.csv`**, **`data/inputs/projects_finance.csv`** — externally sourced project tables (not produced by the flatten/translate pipeline).
- **`data/derived/ficha_idi_table.csv`** — Spanish-only flatten from parsed JSON.
- **`data/derived/ficha_idi_table_translated.csv`** — bilingual ES + EN table (default output of script 03 with translation cache).
- **`data/derived/translations_es_en.json`** — Spanish→English string cache from script 04.

## Mage finance-project export

Run the matcher and then build the upload bundle:

```sh
/Users/amandaeames/Documents/gitrepo/CityCatalyst-global-data/.venv/bin/python scripts/06_match_to_actions.py
/Users/amandaeames/Documents/gitrepo/CityCatalyst-global-data/.venv/bin/python scripts/07_export_finance_project_inputs.py
```

The ignored local `data/pipeline/` directory then contains the two exact S3 objects
read by `cl_finance_project_to_modelled`:

- `cl_ssg_projects.csv` → `raw_data/cl_ssg/cl_ssg_projects/release/v1/cl_ssg_projects.csv`
- `cl_ssg_projects_action_matches.csv` → `raw_data/cl_ssg/cl_ssg_projects/release/v1/cl_ssg_projects_action_matches.csv`

`manifest.json` records row counts and SHA-256 checksums. The action-link file uses a
reviewed crosswalk: rank-1 `strong` candidates form the baseline; documented semantic
false positives are removed; and explicitly reviewed similar-project links are added
where they give an action a genuine precedent. The matcher retains all other ranked
candidates in `data/derived/project_action_matches.csv` for QA; they are not uploaded.
`action_precedent_audit.csv` records a decision for all 102 actions: either a reviewed
BIP precedent is linked, or no project is claimed as a precedent.

### City-facing precedent display

The database confidence vocabulary is technical; display it to a city user as:

- **Similar projects** — `confidence = strong`. These are the default project list and
  are the only BIP records suitable for direct cost or delivery benchmarking.
- **Related projects** — `confidence = goal_aligned`. Show these only in a separate,
  expandable section labelled *“addresses a related goal; not the same intervention”*.
  Never combine them with the similar-project count or a cost benchmark.
- **No direct precedent in this BIP review** — no `strong` rows. Do not fill this state
  with a broad sector match; if related rows exist, show them as optional context.

Use the `rationale` field as the one-sentence explanation below each project card.

After uploading both CSVs to the paths above, trigger Mage pipeline
`cl_finance_project_to_modelled` with `source_release_version: v1` (and the bucket
containing the objects). Its data branch loads `finance_project`; its action branch
loads `finance_project_action` from the separate match file.

For AWS CLI, set the target bucket once and run:

```sh
SOURCE_BUCKET=your-source-bucket
aws s3 cp data/pipeline/cl_ssg_projects.csv \
  "s3://${SOURCE_BUCKET}/raw_data/cl_ssg/cl_ssg_projects/release/v1/cl_ssg_projects.csv"
aws s3 cp data/pipeline/cl_ssg_projects_action_matches.csv \
  "s3://${SOURCE_BUCKET}/raw_data/cl_ssg/cl_ssg_projects/release/v1/cl_ssg_projects_action_matches.csv"
```

Before triggering Mage, compare the uploaded object checksums or sizes with
`data/pipeline/manifest.json`. In the Mage run configuration, use the same
bucket as `source_bucket` and keep `source_release_version` as `v1`; do not
upload the QA candidate file (`data/derived/project_action_matches.csv`).

## Regenerable outputs

`data/derived/` (except externally supplied inputs copied there) and `corpus/parsed/` contain pipeline outputs that can be regenerated from `corpus/pdfs/` and `data/inputs/` (plus external `bip_database.csv` when using the rebuild script).
