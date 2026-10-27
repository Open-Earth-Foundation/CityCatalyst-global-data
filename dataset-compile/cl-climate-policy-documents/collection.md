# cl-climate-policy-documents — collection notes

Provenance and method for the compiled dataset in this folder. Staging dataset:
manufactured from public sources, not ingested, not yet vetted through dataset-review.

## What this is

The **inventory layer** of Chile's climate-policy document universe — one row per
policy or climate-relevant planning instrument. Compiled **fresh from public sources
to test the dataset-compile method** against the `cl-climate-policy.md` context map,
deliberately **independent of the existing cl-ssg review data**. It is the Chile
counterpart of `br-climate-policy-documents`, built to the same schema so the two
countries are directly comparable.

The **rollup dimension is the policy stack tier** (`stack_tier`): `ndc`,
`framework-law`, `long-term-strategy`, `sector-plan-mitigation`,
`sector-plan-adaptation`, `parcc`, `paccc`, `territorial-plan`, `environmental-program`.
Chile is the **inheritance case**: the LMCC (Ley 21.455) legally mandates the cascade
ECLP -> sectoral plans -> regional PARCC -> communal PACCC, so applicability is a clean
scale rule (national=all, PARCC=its region, PACCC=its commune) — the contrast with the
Brazil compile's enumeration case. Facet axes (`source_level`, `document_type`,
`strand`, `sector`, `region_code`/`region_name`/`territory_code`, `status`) back a
general `get_policy_documents(...)` query.

## How it was collected

1. Navigated by the Chile policy landscape map (knowledge-base), which named the stack.
2. Three targeted research passes: national instruments; the sectoral mitigation +
   adaptation plans; and PARCC/PACCC/territorial/PRAS coverage.
3. Fetched primary sources (UNFCCC PDF, LeyChile XML, MMA + ministry pages, GORE
   resolutions, Diario Oficial, municipal PDFs). See sources.yaml.
4. Structured into schema.json; region facts to references/cl-region-codes.csv.
5. Reconciled tier counts to control totals.

## Provenance is a gradient

- `stack_tier` — **derived** (rollup): from level + document_type per the stack.
- `strand` — **derived**: sectoral plans carry their family; frameworks/PARCC/PACCC
  cross-cutting; territorial classes na.
- `region_name` — **derived-by-rule** via references/cl-region-codes.csv.
- `territory_code` — **derived-by-rule**: level_region_commune, built from
  source_level + region_code (commune segment 000 pending an INE commune-code lookup).
- `title_es`, `publisher`, `law_ref`, `publication_year`, `status`, `source_url` —
  **sourced**.
- `verified`, `confidence`, `notes` — **meta**.

## Verification status

- **National (3): fully verified.** NDC 2025 (UNFCCC), LMCC (LeyChile XML + govt PDF),
  ECLP (MMA page).
- **Sectoral plans (18): counts verified, most instruments fetched.** Reconcile to the
  framework: **7 mitigation** (LMCC Art. 8 ministries) and **11 adaptation** sectors
  (9 legacy PANCC + Mineria + Zonas Costeras per ECLP). Caveat: 5 ministries issued a
  single **combined mitig+adapt decree** (Energia DS 91/2024, Mineria DS 24/2025,
  Transporte, MOP-Infraestructura, MINVU-Ciudades DS 40/2024) — split into two rows to
  fit the two-strand schema and flagged in notes, so the physical-document count is
  lower than the row count. Weakest cells (verified=false): Salud mitigation
  (not published), Turismo adaptation (URL), Zonas Costeras (no plan/ministry).
- **PARCC (16): all rowed with status.** Control total from the **CGR audit (Oct 2024):
  4/16 approved** (Atacama, O'Higgins, Los Rios, Los Lagos). Later approvals confirmable:
  RM, Antofagasta (high), Coquimbo, Nuble (med, pending final resolution) -> 8 marked
  in-force. The Los Rios PARCC URL is shared with Los Lagos in the MMA repository —
  flagged (verified=false) for a distinct-PDF check.
- **PACCC (11): sample, honestly partial.** 9 individually-confirmed communes + 2
  region aggregate rows (Los Rios 12/12, Nuble 6). Control: **~22/345 communes (~6%)**
  had a PACCC by Mar 2025 (CGR), against the LMCC Art. 12 deadline of 13-Jun-2025.
- **Territorial (4) + PRAS (3): classes and programmes.** Territorial instruments rowed
  as CLASSES (PNOT/PROT/PRI/PRC), not per-territory documents. 3 PRAS territories
  (Huasco, Quintero-Puchuncavi, Coronel).

## Insights — what the data says (and how Chile compares to Brazil)

- **The method transfers cleanly.** Same schema, same rollup, same control-total
  discipline produced a coherent Chile inventory — the country-agnostic model holds.
- **Chile's cascade shows up as fuller subnational coverage than Brazil's.** Because the
  LMCC *mandates* a PARCC per region and a PACCC per commune, the regional tier is fully
  enumerable (16/16 rowed, ~8 approved and climbing) and communes are actively producing
  plans — versus Brazil, where subnational climate plans are voluntary and sparse. This
  is the inheritance-vs-enumeration contrast made concrete in data.
- **But the mandate outruns delivery.** Only ~half the regions have an approved PARCC
  and ~6% of communes a PACCC, despite a mid-2025 legal deadline — the lopsidedness is a
  compliance gap, not an absence of obligation.
- **Combined decrees are a Chile-specific modelling wrinkle.** Unlike Brazil's separate
  mitigation and adaptation plans, Chile increasingly issues one decree covering both —
  so document count and (sector x strand) count diverge. Flagged per row.
- **Sector coverage is near-complete at national level** (mitigation 7/7 mandated,
  adaptation 9 legacy vigente + 2 emerging), the deepest, most stable tier — the safe
  spine, exactly as the map predicted.

## Known gaps (the to-proper checklist)

1. **Resolve the PACCC sample to per-commune rows** with individual sources (currently 2
   regions are aggregate rows), and refresh the ~22/345 control against any newer audit.
2. **Track all 16 PARCC approvals** to their final Delegado resolution; fix the Los Rios
   vs Los Lagos shared-URL ambiguity.
3. **Fetch the combined-decree PDFs** (Energia, Mineria, Transporte, Infraestructura,
   Ciudades) to source-read exact titles and confirm the mitig/adapt split.
4. **Pin the weak cells**: Salud mitigation, Turismo adaptation, Zonas Costeras.
5. **Enumerate territorial instances** (PROT per region, PRC per commune) if the coverage
   view needs them, replacing the class-level placeholder rows.
6. **Add INE commune codes** to territory_code (commune segment currently 000).
7. **Promote `strand`/`stack_tier` derivations to documented rules** before review.

## Refresh model

No feed. Refresh = re-run the three research passes against sources.yaml and diff.

## Promotion

Graduates into dataset-review when the PACCC sample is resolved per-commune, all PARCC
approvals are tracked, combined-decree titles are source-read, and provenance is
complete. Review then wires it to the LMCC-cascade coverage layer that turns this
inventory into a per-city policy environment.
