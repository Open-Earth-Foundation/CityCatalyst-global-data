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
7. `python scripts/07_enrich_qa_eval.py`

## Key data files

- **`data/inputs/actions.csv`** — action library for matching.
- **`data/inputs/gpc_mapping_v1.csv`** — sector/subsector → GPC mapping.
- **`data/inputs/projects.csv`**, **`data/inputs/projects_finance.csv`** — externally sourced project tables (not produced by the flatten/translate pipeline).
- **`data/derived/ficha_idi_table.csv`** — Spanish-only flatten from parsed JSON.
- **`data/derived/ficha_idi_table_translated.csv`** — bilingual ES + EN table (default output of script 03 with translation cache).
- **`data/derived/translations_es_en.json`** — Spanish→English string cache from script 04.

## Regenerable outputs

`data/derived/` (except externally supplied inputs copied there) and `corpus/parsed/` contain pipeline outputs that can be regenerated from `corpus/pdfs/` and `data/inputs/` (plus external `bip_database.csv` when using the rebuild script).
