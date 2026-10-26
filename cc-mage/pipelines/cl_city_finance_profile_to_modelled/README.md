# Pipeline: cl_city_finance_profile_to_modelled

Loads the reviewed v4 CITY layer into `modelled.city_finance_profile`: fiscal autonomy from SIM/BEP
IPP and FCM plus SSG-supplied other permanent income, alongside the INE-derived technical-capacity
tier for all 345 comunas. The modelled table and score-function contract are unchanged. The v4 input
is programme-use only and is not cleared for commercial use. Migration: global-api revision
`b8e2f5a1c9d4`.

## Flow

```
load_cl_city_action_fundability_from_s3 (reviewed v4 CSV) \
load_cl_ocha_ab_locode_from_s3 (locode lookup)             >- transform_city_finance_profile
        |                                                         validate axes and 0.5 archetype bands
        |                                                         preserve reviewed autonomy/capacity
        |                                                         actor_id = locode
        v
export_city_finance_profile_to_raw -> raw_data.city_finance_profile_staging (replace)

CATALOG branch: load_city_finance_profile_catalog (index.yaml) -> export -> load_dataset_release_city_finance_profile

both branches:
load_city_finance_profile_modelled (transactional hard delete + insert; city_profile_id = MD5(actor_id-release_id))
        v
drop_city_finance_profile_staging
```

## What it produces

345 city profiles. The reconciled OCHA 2021 locode lookup resolves every reviewed comuna. The v4
snapshot after locode resolution is:

- Support-ready: 150
- Delivery-ready: 104
- Self-sufficient: 66
- Well-resourced: 25

## Notes / decisions

- **No axis is recomputed in Mage.** The v4 CSV is the reviewed join and the transformer asserts that
  all 345 rows are complete, numeric, in range, unique by CUT, and correctly banded.
- **actor_id = city locode** via cl-ocha-ab (CL + comuna_cut, padded to 5 digits). actor_id is the API
  key and NOT NULL; the reconciled lookup covers all 345 reviewed comunas.
- **Identity from the catalog** (`oef/cl-city-action-fundability`, v4), with deterministic
  city_profile_id = MD5(actor_id-release_id).
- **Hard replacement is explicit and atomic.** The modelled SQL deletes both the retired
  `cl-subdere/cl-subdere-sinim` rows and any prior OEF city-profile rows inside the same transaction,
  inserts v4, and raises if row counts differ or any retired row remains.
- SQL blocks set disable_query_preprocessing: true so pipeline variables coexist with raw SQL.
- This makes the score endpoint flip from neutral-fallback to profiled per city (design section 8, Phase 2).

## S3 input

- Bucket variable: `source_bucket` (default `test-global-api`)
- Key: `raw_data/oef/cl_city_action_fundability/release/v4/cl_city_action_fundability.csv`
- Local reviewed file to upload: `dataset-review/reviews/oef/cl-city-action-fundability/releases/v4/data/city_finance_profile.csv`

Upload the local file under the key above; the S3 filename is deliberately the catalog dataset slug.
The loader requires the seven modelled-contract columns and exactly 345 unique five-digit CUT codes;
the additional v4 audit columns are retained in the reviewed artifact but not loaded to modelled.

S3 object lifecycle is outside this pipeline. The hard replacement applies to
`modelled.city_finance_profile`: the pipeline never reads the retired SINIM object and does not
delete source objects from S3.
