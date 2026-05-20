# MapBiomas Chile — Collection 2.0 review (in progress)

**Status:** initial scoping — not production-approved.

## What this release is

[MapBiomas Chile Collection 2.0](https://chile.mapbiomas.org/) is an annual **land cover and land use (LULC)** raster time series for the national territory, **1999–2024**, at **30 m** resolution with a **17-class** legend. Collection 2.0 was launched in **October 2025** (replacing Collection 1.0, 2000–2022, 13 classes).

The product is aimed at **territorial analysis** (regions, provinces, comunas, watersheds, protected areas) rather than parcel-level land management.

## Canonical identifiers

| Item | Value |
|------|--------|
| GEE asset | `projects/mapbiomas-chile/assets/LULC/COLLECTION-02/CLASSIFICATIONS/classification-final/clasificacion-final-2` |
| Band semantics | One band per year; band order follows the series (band 1 = first year of the stack) |
| Per-year GeoTIFF (GCS) | `https://storage.googleapis.com/mapbiomas-public/initiatives/chile/coverage/chile_coverage_{YEAR}.tif` |
| Web UI | https://plataforma.chile.mapbiomas.org/ |

Source pages: [Herramientas / GEE](https://chile.mapbiomas.org/en/herramientas/), [Mapas de la colección](https://chile.mapbiomas.org/en/mapas-de-la-coleccion/).

## Review checklist

### Source and license

- [ ] Read current [terms of use](https://chile.mapbiomas.org/) and record `license` block in `review.yaml`
- [ ] Confirm whether CityCatalyst ingestion qualifies as non-commercial / public interest
- [ ] Capture citation string from MapBiomas Chile communications materials

### Technical access

- [ ] Verify GEE asset loads in Code Editor with a standard test comuna geometry
- [ ] Document band index → calendar year mapping for Collection 2.0
- [ ] Test one-year GCS GeoTIFF download and CRS / compression metadata
- [ ] Check GEE user-toolkit maintenance status for comuna-level export

### Legend and semantics

- [ ] Import legend codes from [Leyenda2025 PDF](http://chile.mapbiomas.org/wp-content/uploads/sites/13/2025/10/Leyenda2025-LEYENDA-CODIGOS.pdf) into `data/legend_collection_02.csv` (planned)
- [ ] Draft crosswalk: MapBiomas class → internal indicators (forest, agriculture, urban, water, etc.)
- [ ] Note differences vs Collection 1.0 if any downstream product still references v1

### City integration

- [ ] Define zonal-stats workflow (GEE vs platform CSV) and output grain (comuna vs actor_id)
- [ ] Align admin boundaries with existing Chile polygon sources (INE / OSM / internal `modelled.city_polygon`)
- [ ] List candidate indicators for HIAP / context / AFOLU (e.g. natural cover share, urban expansion rate)

### Samples and QA

- [ ] Add `sample/` extracts for 1–2 comunas × 2 years (area by class)
- [ ] Optional: `notebook/exploration.ipynb` for GEE smoke test
- [ ] Spot-check against platform statistics for the same units

## Collection comparison (working notes)

| | Collection 1.0 | Collection 2.0 |
|---|----------------|----------------|
| Years | 2000–2022 | 1999–2024 |
| Classes | 13 | 17 |
| GEE asset (v2) | TBD — document if needed | `…/clasificacion-final-2` |

Do **not** concatenate statistics across collections without a documented crosswalk.

## Next steps

1. Complete legend CSV under `data/`.
2. Run GEE zonal-stats prototype for a pilot comuna (e.g. Valdivia / Santiago).
3. Update `catalog/index.yaml` `production_approved` only after license + sample QA sign-off.
