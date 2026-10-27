# Pipeline: cl_finance_opportunity_to_modelled

Loads the Chile supply inventory into `modelled.finance_opportunity` (table 1 of the
Chile climate-finance model). Design: `dataset-review/reviews/oef/cl-city-action-fundability/releases/v1/implementation.md`;
field audit: see the implementation doc.

## Flow

```
DATA branch:
load_<source>_finance_from_s3 (py) × 10   one thin ingestion block per source:
        │                                 read its own S3 raw_data file, tag _source_dataset
        ▼
merge_finance_opportunity (transformer)   integrate: align to the audited superset,
        │                                 unmodeled cols → source_extras, union + dedupe
        ▼
export_finance_opportunity_to_raw (py)    → raw_data.finance_opportunity_staging (replace)

CATALOG branch (identity from index.yaml — no per-dataset variables):
load_finance_source_catalog (py)          read the 10 source entries from dataset-review/catalog/index.yaml,
        │                                 compute publisher_id / dataset_id / release_id per source
        ▼
export_finance_source_catalog_to_raw (py) → raw_data.finance_source_catalog (replace)
        ▼
load_dataset_release_finance_opportunity (sql)  upsert ONE publisher_datasource + dataset_release per source

both branches ▼
load_finance_opportunity_modelled (sql)   join staging → finance_source_catalog on source_dataset so each
        │                                 row carries ITS OWN source release_id; release-scoped DELETE+INSERT.
        │                                 ids: release_id = MD5(datasource·dataset·version) (no dataset_url);
        │                                 opportunity_id = MD5(source_opportunity_id·release_id)
        ▼
drop_finance_staging (sql)                final cleanup — DROP raw_data.finance_opportunity_staging
                                          and raw_data.finance_source_catalog (throwaway)
```

## What it produces

99 opportunities from 10 reviews (cl-mma 55, cl-indap 9, cl-mop 7, cl-minenergia 6,
cl-corfo 5, cl-subdere 4, cl-minvu 4, cl-gore 4, cl-mtt 3, cl-conaf 2). Channels:
89 competitive · 7 public-investment (BIP-SNI-gated: FNDR/FRIL/FRPD + SUBDERE) · 3 intermediated (MTT).

## Notes / decisions

- **Nothing dropped.** Every review column maps to a modelled column or rides in
  `source_extras` (JSONB). Two DQ flags (`amount_suspect`, `status_section_conflict`)
  fold into `data_quality_flags`.
- **INDAP** ships a fund→action *mapping* file (14 rows = 9 funds repeated); the loader
  dedupes to one opportunity per fund. The per-action mapping is the action layer's job
  and is preserved in `source_extras` on the kept row.
- **`funding_channel` / `access_tier` / `city_application` are derived** by heuristic
  (`classify_channel_tier`), because the v1 review CSVs don't yet carry an explicit value.
  Production should curate these in the source review (see design §7.5); the heuristic is
  the documented stand-in.
- **One ingestion block per source, integrated in the merge block** — no pre-aggregation,
  no looping loader. The ten `load_<dataset_key>_finance_from_s3.py` blocks are the source
  manifest (the DAG lists them); each reads its own
  `raw_data/<publisher_key>/<dataset_key>/release/<version>/<dataset_key>.csv` via the Mage
  `S3` loader (`source_bucket` / `source_release_version` are pipeline variables).
  `mappings/sources.csv` is now superseded by these blocks and is no longer read.
- **Field renames are an inline `SYNONYMS` dict in `transformers/merge_finance_opportunity.py`**
  (the superset is derived from its distinct targets). Inlined because Mage blocks read no
  local-repo files (no `__file__`); if it grew large it would move to S3, not a repo CSV.
  The earlier `mappings/field_synonyms.csv` and `mappings/sources.csv` are superseded and unused.
- **Each row carries its own source dataset's `release_id`** — not one inventory release.
  Identity comes from `index.yaml` (the catalog branch): one `publisher_datasource` +
  `dataset_release` is registered per source (10 of them), and each opportunity row joins
  to its source on `source_dataset`. So provenance, license and version are per-source.
- **Identity from the catalog, not pipeline variables.** `load_finance_source_catalog`
  fetches `index.yaml` from GitHub raw (`CATALOG_INDEX_URL`, overridable via the
  `catalog_index_url` kwarg), so there are no per-dataset variables — the pipeline has just
  two (`source_bucket`, `source_release_version`). Adding a source = add its `index.yaml`
  entry + a loader block.
- **Idempotent**: release-scoped `DELETE` + `INSERT` (deletes the affected source releases'
  rows, then rebuilds) with deterministic `release_id = MD5(datasource·dataset·version)`
  (no `dataset_url`) and `opportunity_id = MD5(source_opportunity_id·release_id)`.
