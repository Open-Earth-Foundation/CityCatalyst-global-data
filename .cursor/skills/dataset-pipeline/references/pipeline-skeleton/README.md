# Pipeline skeleton

Copy this into place and replace every `<…>` token:

```
cc-mage/pipelines/<PIPELINE_NAME>/metadata.yaml   ← metadata.yaml
cc-mage/data_loaders/load_<SOURCE>_staging.py     ← data_loaders/load_SOURCE_staging.py
cc-mage/data_exporters/export_<SOURCE>_to_raw.py  ← data_exporters/export_SOURCE_to_raw.py
cc-mage/data_exporters/export_<SOURCE>_modelled.sql ← data_exporters/export_SOURCE_modelled.sql
cc-mage/data_exporters/drop_<SOURCE>_staging.sql  ← data_exporters/drop_SOURCE_staging.sql
cc-mage/pipelines/<PIPELINE_NAME>/triggers.yaml   ← triggers.yaml (API trigger <PIPELINE_NAME>_api)
```

Mappings: a field/category map is inline in the block if small, or in S3 (loaded
like the data) if large — never a local-repo CSV (Mage blocks have no `__file__`).

Tokens: `<PIPELINE_NAME>` = `<prefix>_<source>_<description>`, `<SOURCE>` = the
short source key, `<MODELLED_TABLE>` / `<PK>` / `<natural_key>` = the target
table's name, primary key, and source natural key.

These are the generic single-source templates. For the full standard pattern —
the **catalog branch** (reads `index.yaml` from GitHub → registers a `dataset_release`
per source), **per-source ingestion blocks + a merge** when there are several sources,
and each row carrying its own source `release_id` — copy from the worked reference
pipeline `cc-mage/pipelines/cl_finance_opportunity_to_modelled/` (blocks
`load_finance_source_catalog`, `load_dataset_release_finance_opportunity`,
`merge_finance_opportunity`). The `how` for each piece is in
`knowledge-base/topics/engineering-standards/`.
