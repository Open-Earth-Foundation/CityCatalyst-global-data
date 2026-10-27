# MapBiomas Chile — land use and land cover (LULC)

Annual **land cover and land use** maps for Chile from the [MapBiomas Chile](https://chile.mapbiomas.org/) collaboration network. Maps are produced with remote sensing on the [Google Earth Engine](https://earthengine.google.com/) platform (technological partner: [Seeg](https://seeg.org/)).

## Why we track it

- **National LULC time series** — annual rasters for the full Chilean territory support land-based indicators (forest/natural cover, agriculture, urban expansion, water, change detection).
- **City-relevant aggregation** — platform statistics and GEE tooling support **region, province, comuna**, watershed, and protected-area units (aligns with Chilean admin boundaries used elsewhere in CityCatalyst).
- **GEE-native access** — no bulk download required for exploration; multi-year stacks are a single multi-band asset.

## Current review release

**Collection 2.0** (1999–2024, 17 legend classes) — see [`releases/collection-02/`](releases/collection-02/).

Collection 1.0 (2000–2022, 13 classes) remains on the site for comparison; this review focuses on Collection 2.0 unless a downstream use case explicitly requires v1.

## Access paths

| Channel | Notes |
|---------|--------|
| **GEE asset** | `projects/mapbiomas-chile/assets/LULC/COLLECTION-02/CLASSIFICATIONS/classification-final/clasificacion-final-2` — one image, **one band per year** ([tools page](https://chile.mapbiomas.org/en/herramientas/)) |
| **Public GeoTIFF** | `https://storage.googleapis.com/mapbiomas-public/initiatives/chile/coverage/chile_coverage_{YEAR}.tif` ([collection maps](https://chile.mapbiomas.org/en/mapas-de-la-coleccion/)) |
| **Web platform** | [plataforma.chile.mapbiomas.org](https://plataforma.chile.mapbiomas.org/) — maps, change, statistics, exports |
| **Legend** | [Collection 2.0 codes (PDF)](http://chile.mapbiomas.org/wp-content/uploads/sites/13/2025/10/Leyenda2025-LEYENDA-CODIGOS.pdf), [descriptions EN (PDF)](http://chile.mapbiomas.org/wp-content/uploads/sites/13/2025/10/Leyenda2025-EN-LEYENDA-DESCRIPCIONES.pdf) |

## Known strengths

- Long annual series (Collection 2.0: **1999–2024**)
- **30 m** resolution, full national extent
- Consistent MapBiomas network methodology; ATBD and glossary on the site
- Multiple access modes (GEE, GCS, platform)

## Known limitations

- Recommended cartographic scale **up to 1:100,000** (not parcel-level)
- Class legend and methodology **differ between Collection 1 and 2** — do not mix without a crosswalk
- GEE user toolkit for subnational clip/export was **under maintenance** at last check ([collection maps page](https://chile.mapbiomas.org/en/mapas-de-la-coleccion/))

## License

[CC BY 4.0](https://chile.mapbiomas.org/uso-de-datos/) — "Los datos de MapBiomas son de uso público, abierto y gratuito, sujetos a citación." Commercial use, redistribution and derivatives permitted; citation required.

## Links

- Site: https://chile.mapbiomas.org/
- Products: https://chile.mapbiomas.org/en/productos/
- Downloads: https://chile.mapbiomas.org/en/descargas/
- Methodology: https://chile.mapbiomas.org/en/metodologia/
