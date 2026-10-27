# Chile Administrative Boundaries (COD-AB)

[Chile - Subnational Administrative Boundaries](https://data.humdata.org/dataset/cod-ab-chl) on the Humanitarian Data Exchange (HDX), published by OCHA as a Common Operational Dataset (COD).

## Why we use it
- **City boundaries** — Comuna (admin 3) polygons for spatial joins, mapping, and city context
- **Region/province** — Admin 1 (16 regions) and Admin 2 (56 provinces) for hierarchical lookup
- **Join keys** — P-codes and standardised names for linking with census, CASEN, UNLOCODE

## Data
- **Admin 1:** 16 regions
- **Admin 2:** 56 provinces  
- **Admin 3:** 345 comunas

The release also carries a 346-row CUT-to-LOCODE crosswalk at
`releases/2021/data/chile_comunas.csv`. The pipeline-ready spatial artifacts
contain the 345 OCHA polygons joined to that crosswalk. Antártica (`CL12202`) is
the sole crosswalk row without an OCHA 2021 polygon and is not fabricated in the
spatial output.

Formats: Shapefile (SHP), GeoJSON. Sample: GeoPackage. Last valid for humanitarian use: Oct 2021.

## Current approved release
**2021**

## Main sources
- [HDX: Chile COD-AB](https://data.humdata.org/dataset/cod-ab-chl)
- [OCHA COD-AB documentation](https://data.humdata.org/dashboards/cod?dataseries_name=COD+-+Subnational+Administrative+Boundaries)
