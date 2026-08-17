# Chile comuna LOCODE gap report

Date checked: 2026-08-16

## What the current file contains

The current OCHA mapping has 345 rows:

| Result | Comunas |
|---|---:|
| Direct name match | 329 |
| Clear spelling or source-name variant | 2 |
| LOCODE taken from a related place | 10 |
| No LOCODE stored | 4 |
| **Total** | **345** |

The 10 related-place matches are why counting only blank fields gives an incomplete picture.

## The 10 related-place matches

| Comuna | LOCODE currently used | LOCODE place name | Finding |
|---|---|---|---|
| Aysén | `CL PSN` | Puerto Aysen | Related locality, not the comuna name. |
| Laja | `CL LAJ` | La Laja | Related locality/name variant. |
| Los Andes | `CL LIB` | Paso Cristo Redentor-Los Libertadores/Los Andes | Border crossing. Use `CL LND` for Los Andes instead. |
| Mostazal | `CL MOS` | San Francisco de Mostazal | Related locality, not the comuna name. |
| Natales | `CL CVJ` | Paso Laurita Casas Viejas/Puerto Natales | Border crossing. `CL PNT` for Puerto Natales is a better related-place match. |
| Puyehue | `CL CSA` | Paso Cardenal A. Samoré/Puyehue | Border crossing. Use `CL PYH` for Puyehue instead. |
| Quellón | `CL PTE` | Quellón (Puerto Quellón) | Related port/locality. |
| Rinconada | `CL RIN` | Rinconada de Los Andes | Related locality, not the comuna name. |
| Río Hurtado | `CL RHU` | Hurtado | Related locality, not the comuna name. |
| Santo Domingo | `CL RSD` | Rocas de Santo Domingo | Related locality. Use `CL SDO` for Santo Domingo instead. |

These rows should not be presented as exact comuna-to-LOCODE matches. They are either related-place links or incorrect selections made by the automated spatial match.

## Blank rows and missing comunas

| Comuna | CUT code | Finding | Recommended treatment |
|---|---:|---|---|
| Pozo Almonte | 01401 | The boundary file incorrectly has a second Tocopilla row in this position. No direct LOCODE was found. | Correct the boundary row; keep LOCODE empty. |
| Paihuano | 04105 | No direct LOCODE was found. | Keep LOCODE empty. |
| Marchigüe | 06204 | UNECE has `CL MAR` under the spelling "Marchihue". | Use `CL MAR` and record the spelling alias. |
| Cisnes | 11202 | UNECE has `CL CIS` for Puerto Cisnes. | Keep the comuna LOCODE empty; record `CL CIS` as a related locality if useful. |
| Antártica | 12202 | Missing from the OCHA file. No direct comuna-level LOCODE was found. | Add the comuna from an official boundary source; keep LOCODE empty. |

Tocopilla itself is not a gap. Its LOCODE is `CL TOQ`.

## Expected position after corrections

Using all 346 official Chilean comunas:

| Result | Comunas |
|---|---:|
| Clear LOCODE match | 335 |
| Related locality available, but not the same named entity | 8 |
| No usable comuna-level LOCODE | 3 |
| **Total** | **346** |

The eight related-locality cases are Aysén, Cisnes, Laja, Mostazal, Natales, Quellón, Rinconada and Río Hurtado.

The three without a usable comuna-level LOCODE are Pozo Almonte, Paihuano and Antártica.

## Temporary identifier recommendation

Do not invent values that look like official UN/LOCODEs, such as `CL PAI`.

Use the Chilean CUT comuna code with a CityCatalyst namespace:

```text
CL-CUT-01401
```

Format: `CL-CUT-` followed by the five-digit CUT code.

Store this value as an `actor_id` or `temporary_actor_id`. Keep `locode` nullable and only store official UNECE values in it.

## Sources

- [INE: Chile has 346 comunas](https://www.ine.gob.cl/herramientas/portal-de-mapas/geodatos-abiertos/2024/08/01/censo-2024-finaliz%C3%B3-en-las-346-comunas-del-pa%C3%ADs)
- [UNECE: Chile UN/LOCODE list](https://service.unece.org/trade/locode/cl.htm)
- `sample/cl_admin_locode.gpkg` in this release
- `exploration.ipynb` in this release
