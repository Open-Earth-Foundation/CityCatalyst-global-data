# Chile policy documents — SSG curated inventory

Curated inventory of Chilean national, regional, and selected subnational **policy and planning documents** used for MEED / SSG policy-signal and legal-context work. The authoritative row-level manifest is the CSV in the latest release `sample/` folder.

## Why we use it

- Single machine-readable index of **document titles, governance actor, territorial scale, territory codes, and source links** (where available).
- Covers climate instruments (ECLP, sectoral mitigation plans, PARCC, NDC), territorial planning (PNOT, PDU, PDR, regional and communal instruments), and selected environmental programmes (e.g. PRAS).

## Current release

**2026** — initial catalogued inventory (`data_requirements_general_policies.csv`).

## Known strengths

- Explicit **territory coding** (`Territory_code`, region/communal codes where applicable) aligned with internal MEED requirements.
- Mix of **national, regional, communal, and inter-communal** scales in one table.

## Known limitations

- **Heterogeneous publishers** (multiple ministries, GOREs, municipalities); not one API or one license.
- Some rows are **document-type placeholders** (e.g. “*1 per Region*”, “*1 per Communa*”) without a stable URL.
- **Access and terms** differ by host (government sites, SharePoint, Google Drive, portals); confirm reuse before redistribution of full PDFs.
- One regional PARCC entry may be **in process** or link to a flipbook rather than a single PDF.

## Links

- National climate hub (representative): https://cambioclimatico.mma.gob.cl/
