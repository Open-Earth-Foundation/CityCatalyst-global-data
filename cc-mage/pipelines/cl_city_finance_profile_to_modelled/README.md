# Pipeline: cl_city_finance_profile_to_modelled

Loads the CITY layer into `modelled.city_finance_profile` (design section 5.1) -- the financial
autonomy and delivery capacity axes the score reads, per city. Source: the SUBDERE/SINIM review
(cl-subdere-sinim, 345 comunas). Migration: global-api revision `b8e2f5a1c9d4`.

## Flow

```
load_cl_subdere_sinim_from_s3 (bare S3 read)   \
load_cl_ocha_ab_locode_from_s3 (locode lookup)  >- transform_city_finance_profile
        |                                              autonomy = clip(1 - fcm_dependency_pct/100, 0, 1)
        |                                              capacity = 0.7*pctrank(staff_profesional_total)
        |                                                       + 0.3*pctrank(professionalization_pct)
        |                                              city_archetype banded at 0.5; actor_id = locode
        v
export_city_finance_profile_to_raw -> raw_data.city_finance_profile_staging (replace)

CATALOG branch: load_city_finance_profile_catalog (index.yaml) -> export -> load_dataset_release_city_finance_profile

both branches:
load_city_finance_profile_modelled (release-scoped DELETE+INSERT; city_profile_id = MD5(actor_id-release_id))
        v
drop_city_finance_profile_staging
```

## What it produces

~341 city profiles (of 345 comunas; 4 dropped for having no locode -- not queryable by the score
endpoint). autonomy/capacity in [0,1] (validated to reproduce the methodology fixture exactly).
archetype split (city-facing, strength-based): Support-ready ~157, Delivery-ready ~99, Self-sufficient ~61, Well-resourced ~24.

## Notes / decisions

- **autonomy / capacity formulas** are the methodology blend (02_fundability_model.ipynb), computed in
  the transformer over the full 345-row frame (capacity is a percentile rank, so it needs all rows).
  Validated against the methodology fixture (max abs diff 0.005, just its 2-dp rounding) before that fixture was removed.
- **actor_id = city locode** via cl-ocha-ab (CL + comuna_cut, padded to 5 digits). actor_id is the API
  key and NOT NULL, so the 4 comunas without a locode are dropped.
- **Identity from the catalog** (cl-subdere-sinim), per-source release_id; deterministic
  city_profile_id = MD5(actor_id-release_id); idempotent release-scoped delete+insert.
- SQL blocks set disable_query_preprocessing: true so pipeline variables coexist with raw SQL.
- This makes the score endpoint flip from neutral-fallback to profiled per city (design section 8, Phase 2).
