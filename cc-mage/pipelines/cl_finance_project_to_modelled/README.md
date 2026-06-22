# Pipeline: cl_finance_project_to_modelled

Loads the Chile precedent layer into `modelled.finance_project` (table 2 of the Chile
climate-finance model). Design: `dataset-review/reviews/oef/cl-city-action-fundability/releases/v1/implementation.md`
(sections 3.2 amounts/units, 4.2 funding_sources JSONB). Migration: `global-api` revision
`a4f1c9d72b3e`. Mirrors the worked reference `cl_finance_opportunity_to_modelled`.

## Flow

```
DATA branch (per-source bare S3 loaders -> one merge):
  load_cl_ssg_projects_from_s3 (BIP projects)        \
  load_gcf_projects_from_s3                            >- merge_finance_project (transformer)
  load_cl_mma_fpa_awards_from_s3                      /      shape per source, caps-normalize,
  load_cl_conaf_bn_awards_from_s3                    /       English base + i18n {es,en},
  load_cl_ocha_ab_locode_from_s3 (locode lookup)    /        funding_sources JSONB, locode join
        |
        v
  export_finance_project_to_raw -> raw_data.finance_project_staging (replace)

ACTION branch (project<->action links; same project loaders + the BIP matches loader):
  load_cl_ssg_project_matches_from_s3 + the 4 project loaders
        v
  transform_finance_project_action (BIP per-project matches + GCF/FPA/CONAF grain crosswalks;
        several links per project, e.g. CONAF -> up to 3 actions; confidence strong/goal_aligned)
        v
  export_finance_project_action_to_raw -> raw_data.finance_project_action_staging (replace)

CATALOG branch (identity from index.yaml, per-source release_id):
  load_finance_project_catalog (GitHub raw index.yaml, 4 source ids, MD5 ids)
        v
  export_finance_project_catalog_to_raw -> raw_data.finance_project_catalog (replace)
        v
  load_publisher_datasource_from_catalog -> load_dataset_release_from_catalog (per-source upsert)

all branches:
  load_finance_project_modelled (join staging -> catalog on source_dataset; release-scoped
        DELETE+INSERT; project_id = MD5(source_project_id-release_id))
        v
  load_finance_project_action_modelled (FK-safe JOIN finance_project drops orphan links;
        project_action_id = MD5(project_id-action_id-mapping_source))
        v
  drop_finance_project_staging (DROP the throwaway staging + catalog tables)
```

SQL blocks set `disable_query_preprocessing: true` so the pipeline variables coexist with raw SQL
without Mage Jinja conflicts (the SQL uses no Jinja). Variables: `source_bucket`,
`source_release_version` (the 4 sources), `locode_release_version` (cl-ocha-ab, 2021).

## What it produces

~11,511 projects (modelled.finance_project) from 4 reviews: CONAF 9,860, FPA 655, BIP (cl-ssg) 988,
GCF 8. Channels: competitive fund (CONAF+FPA), public investment (BIP), intermediated multilateral
(GCF). `actor_id` = city locode where a comuna resolves (FPA ~643, BIP ~476; CONAF/GCF
region/national -> null). Descriptive base columns (project_name, sector) are English; *_i18n keeps
{es, en}.

Action matches land in modelled.finance_project_action (~28,400 links after the FK-safe join drops
orphans), confidence {strong, goal_aligned}, several actions per project allowed (CONAF up to 3).

## Sources (one review each, no pre-aggregation)

| source_dataset | catalog id | raw_data key |
|---|---|---|
| cl-ssg/cl-ssg-projects | cl-ssg-projects | raw_data/cl_ssg/cl_ssg_projects/release/v1/cl_ssg_projects.csv |
| (BIP action matches) | cl-ssg-projects | raw_data/cl_ssg/cl_ssg_projects/release/v1/cl_ssg_projects_action_matches.csv |
| gcf/gcf-projects | gcf-projects | raw_data/gcf/gcf_projects/release/v1/gcf_projects.csv |
| cl-mma/cl-mma-fpa-awards | cl-mma-fpa-awards | raw_data/cl_mma/cl_mma_fpa_awards/release/v1/cl_mma_fpa_awards.csv |
| cl-conaf/cl-conaf-bn-awards | cl-conaf-bn-awards | raw_data/cl_conaf/cl_conaf_bn_awards/release/v1/cl_conaf_bn_awards.csv |
| (locode lookup) | cl-ocha-ab | raw_data/ocha_rolac/cl_ocha_ab/release/2021/cl_ocha_ab.parquet |

## Notes / decisions

- **Bare loaders, shaping in the merge.** Each loader is a bare S3 read (tagged `_source_dataset`
  for the 4 project sources). The merge identifies the BIP-match and locode frames by their columns.
- **Caps-normalization in the pipeline.** All-caps source text (BIP names, sectors, institutions) is
  title-cased in the merge; mixed-case text (FPA creative titles) is left as-is. Mojibake repaired
  inline (no ftfy dependency); never by editing source CSVs.
- **i18n.** Translated descriptive fields carry a companion JSONB: `project_name_i18n`,
  `sector_i18n` ({es, en}). English from the review `*_en` columns (BIP `nombre_en`, FPA
  `nombre_proyecto_en`, BIP `sector_en`); CONAF name synthesized + hardcoded EN; GCF native EN.
- **Canonical vocab, off-list dropped.** `match_label` is {strong, goal_aligned} (high->strong,
  medium->goal_aligned; off-list -> null match_label and null action_id). Grain crosswalks
  (GCF/FPA/CONAF) are small inline maps; the BIP per-project match is its own S3 input.
- **No source_extras / speculative columns.** Unmodeled source columns are dropped. `sector` is
  intentionally mixed taxonomy (BIP Spanish vs GPC afolu vs GPC tokens) -- a documented gap.
- **Amounts raw with unit** (CLP_millions / UTM / CLP / USD); cost_total is BIP-fed, FPA/CONAF
  awards -> amount_committed; staged as text and cast in SQL.
- **Identity from the catalog.** One publisher_datasource + dataset_release per source (4), each
  row joins on `source_dataset` to carry its own source release_id.
- **Idempotent**: release-scoped DELETE + INSERT with deterministic
  `release_id = MD5(datasource-dataset-version)` and `project_id = MD5(source_project_id-release_id)`.
- **Variables**: `source_bucket`, `source_release_version` (the 4 sources), `locode_release_version`
  (the cl-ocha-ab lookup, 2021). No per-dataset identity variables.
