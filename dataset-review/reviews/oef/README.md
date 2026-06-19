# OEF — OpenEarth Foundation (internal datasets & models)

This publisher namespace is different from the others under `dataset-review/reviews/`. Every other publisher (`cl-mma`, `ipcc`, `world-bank`, …) is an **external** data source we reviewed. **`oef` is us.** It holds the datasets and analytical products OpenEarth Foundation produces ourselves, rather than ingests from a third party.

## What belongs here

- **Internally curated data** — datasets we assemble by hand or by extraction from many sources (e.g. a climate-finance inventory built from dozens of government pages).
- **Integrated / derived datasets** — products that union, harmonize, or cross-reference several already-reviewed external datasets into one table.
- **Our own models & indicators** — methodologies and scored outputs we design (rankings, coverage indicators, risk layers), with the model logic and its caveats versioned alongside the data.

The defining test: if the *source* of the data is OEF's own curation, integration, or modelling — not an external publisher — it lives here. (For an external source we merely vet, use that publisher's own namespace.)

## Provenance & licence — important

Because these are derived / our own, two rules apply:

- **Authority lives upstream.** When an OEF product is built from external reviews, those source reviews remain authoritative for provenance and licence. The OEF entry inherits the most restrictive upstream licence; it does not re-grant rights. Always check the inputs' licences before redistributing an OEF product.
- **Make the derivation reproducible.** An OEF dataset should ship the code that builds it (notebooks) and a `methodology.md` / `review.md` stating what it can and cannot support — so "OEF-curated" never means "unsourced". Prefer extraction / harmonization code over hand-typed values.

## Structure

Each product follows the standard review layout — `README.md` (plus a hub `methodology.md` where the product is a working method) at the dataset root, and artefacts under `releases/<version>/` with data in `releases/<version>/data/` and a release `review.md`.

## Contents

- `cl-city-action-fundability/` — Chile **city-action fundability** (the consolidated product; supersedes the former `cl-finance-inventory` and `cl-action-fundability`). Harmonizes the ten reviewed Chile finance sources into one fund inventory (99 rows) with an action **financing-availability (coverage)** indicator, then combines four layers (action catalog, SINIM/Censo municipal capacity, the inventory, the projects pipeline) into a per (action × comuna) **route/effort label + matched funds** feeding MEED+ HIAP Feasibility — plus a traceable `finance_db` fixture that makes the three access routes explicit. Working methodology; exploratory / pre-Mage.

## Status

Most OEF products here are **research / exploratory** (not production-approved, not yet in a Mage pipeline). Promotion to the production pipeline + `catalog` / `knowledge-base` happens once a product's methodology stabilises.
