# Review Notes — v2 (IPPU & AFOLU)

## What this release is

v2 covers the **IPPU** (Industrial Processes and Product Use, 28 actions) and **AFOLU** (Agriculture, Forestry and Other Land Use, 24 actions) sectors — 52 OEF catalogue actions in total. It is delivered as a single workbook (`MEED_IPPU_AFOLU 21.05.2026 VF.xlsx`) with four tabs: Análisis Cualitativo, Detalle Cuantitativo, Contexto, Referencias.

## Core methodological change from v1

v2 is **not** the same instrument as v1 re-run on new sectors. The unit of measurement changed.

- **v1 (Residuos / Energía / Transporte)** measured *municipal* viability directly: can a municipality implement this action under current Chilean law? Score = `Legal 40% + Governance 30% + Financing 30%`.
- **v2 (IPPU / AFOLU)** measures *national policy alignment*: does Chile already have a live plan/programme/instrument that is the legal-budgetary vehicle for this action — regardless of which level of government executes it? Score = `C1 Instrument (35) + C2 Institutional mandate (20) + C3 Budget operability (25) + C4 Climate alignment (20)`.

The reframe is deliberate and justified in the methodology: for IPPU and AFOLU the municipality is generally **not** the lead normative actor (competence sits with Min. Energía, MMA, MINAGRI, CORFO, CONAF, INDAP), so a municipal-viability question would mostly return "no" for reasons that have nothing to do with the action's actual feasibility. Municipal role is instead captured separately (Contexto tab + methodology §7).

Other notable shifts:

- New **"explicit instrument" vs "natural vehicle"** distinction drives C1 — the single most judgment-sensitive call in the model.
- New **automatic ceiling**: if C1 = 0 (no operative instrument), the action is capped at 18 points (forced "Baja") no matter how strong C2–C4 are.
- Scoring is described as **fully mechanical** (sum of four components, no discretionary post-adjustment), with the qualitative conclusion driving the component values.
- International grounding is made explicit: OECD Rio Markers / Green Budget Tagging (C3), CAPMF (overall logic), UNDP CPEIR (C1–C3 policy-institution-budget triad).

## Data verification (Detalle Cuantitativo)

I recomputed every row independently:

- **All 52 actions are scored.** Band split matches the executive summary exactly: 10 Alta (≥75), 32 Con condiciones (40–74), 10 Baja (<40).
- **Arithmetic is clean.** For all 52 rows, displayed total = C1+C2+C3+C4, and the C1=0 → cap-18 rule holds with no violations.
- **Component caps respected** (C1≤35, C2≤20, C3≤25, C4≤20) in every row.
- **Band boundaries correct**, including the borderline IPPU-20 = 74 → "Con condiciones" (not rounded up to Alta).

No numerical errors found.

## Main finding — coverage gap between tabs

The quantitative tab scores **all 52** actions, but the qualitative tab (Análisis Cualitativo) only contains **37** rows: all 28 IPPU, but **only 9 of 24 AFOLU**.

AFOLU actions scored **without** a qualitative justification: AFOLU-03, 04, 06, 08, 10, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22 (15 actions).

This matters because the methodology states the qualitative conclusion is what *determines* the score ("los valores de C1–C4 se asignan de forma que la aritmética reproduzca esa conclusión"). For these 15 AFOLU actions the C1–C4 values exist but the narrative basis that is supposed to ground them is not in the workbook. Several of them carry high scores (e.g. AFOLU-13, 16*, 19 = 90; *16 has qualitative), so the gap is not confined to low-stakes rows.

The methodology footnote (§8) acknowledges this — "cubre las 37 acciones … las 15 acciones AFOLU restantes tienen la arquitectura preparada para completar" — but the Resumen Ejecutivo and the quantitative tab present all 52 as final results without flagging which 15 are not yet qualitatively backed. Recommend either (a) marking those 15 rows as provisional in the data, or (b) completing the qualitative analysis before the scores are treated as final.

## Smaller notes

- **Internal version labels are inconsistent.** Filename says v2 / "VF" (versión final); the Detalle tab header says "Fórmula MEED v3", the Contexto tab says "v2.2", and the methodology references a "Nota v2.1". Worth settling on one version string.
- **Municipal role data is richer than the narrative implies.** The Contexto tab codes 25 of 52 actions with a non-null municipal role (Ejecuta 20, Co-financia 3, Recibe transferencia 2). The methodology prose foregrounds "three IPPU actions" with a municipal role; the structured data is broader, which is good, but the two should be reconciled so readers don't under-count.
- **Budget anchoring is point-in-time.** All glosa evidence is anchored to Ley N°21.722 (Presupuestos 2025) and both the Energía and Agricultura PSMs are "proyecto definitivo" pending decree. Scores for those actions (C1/C3) will move upward once the decrees are promulgated — the dataset should be re-versioned at that point rather than edited in place.
- **References verified by the author** against BCN and OECD/Springer DOIs; spot-checks of the cited laws (21.455, 21.305, 21.722, 20.283, 20.920) are consistent.

## Unified legal classification (merge across versions)

This release also carries a cross-version merge: `legal-classification-v2.csv` (with `legal-classification-methodology.md`). It pulls the **legal layer only** from every sector assessment into one file of 100 actions, so the whole OEF catalogue sits on a single legal-feasibility scale. Governance capacity and financing are deliberately excluded — they need real data rather than expert scoring, and they belong as later layers that refine *within* the legal tiers, not folded into the score.

What the merge does and what it means:

- **One verdict, three values.** Every action gets `legal_verdict` = enabled / conditional / blocked, with a short `verdict_desc` gloss in-row. Distribution across the 100 actions: 21 enabled, 50 conditional, 29 blocked.
- **Two honest inputs.** The verdict decomposes into `authority` (is a body legally empowered to act?) and `permission` (does an in-force norm actually permit it, free of prohibition?), each with its own short description field. These replaced the v1 "ownership/restrictions" labels, which didn't carry over cleanly to IPPU/AFOLU — the relabel was verified to change zero verdicts.
- **It is a merge of definitions, not just rows.** v1 asked "can the *municipality* act?"; v2 asks "is there a legal basis at the *responsible level*?" The merge reconciles these by reading authority as competence at whatever level holds it, and tagging each action with `responsible_level` (municipal 12 / shared 43 / national 45). That column is what keeps the two halves from being silently equated.
- **Provenance is preserved.** `source_version`, `source_basis`, and `input_evidence` record where each row's verdict came from (v1 expert review vs v2 C1/C2 derivation) and what evidence backs each axis.
- **What it is for:** a legal *gate/classification* — what is permitted and by whom — not a full feasibility ranking. Legal viability is necessary but not sufficient; an action can be legally enabled yet unfunded (e.g. IPPU-20).

**Blocked actions are triaged, not dropped.** Because "blocked" means "not actionable under current law" (not permanent), each blocked action carries a `city_disposition`: 17 are `hard_filter` (competence sits exclusively with a national regulator/utility — no city lever, hidden to avoid false signaling), and 12 are `show_with_challenge` (4 where the city has a facultative role, 8 national policy gaps surfaced as advocacy dependencies). Net 83 of 100 shown to the city. `block_reason` records which case applies.

Caveats to read alongside it: 15 AFOLU rows are `qualitative_backing = pending` (scored from components, narrative not yet written); one transport action (`ipcc_0105`) has no legal assessment in either source, so coverage is 100 of 101; and `legal_verdict_score` should not be pooled across sectors without `responsible_level` in view.

## Data location

The merged legal classification is loaded to S3 at:
```
s3://test-global-api/raw_data/cl_ssg/cl_ssg_legal_signals/release/v2/legal-classification-v2.csv
```

## Bottom line

The v2 numbers are internally consistent and the methodological reframe from "municipal viability" to "national policy alignment" is sound and well-documented for these two sectors. The one substantive gap before this is treated as a finished dataset is the **15 AFOLU actions that are scored but not qualitatively analysed** — they should be flagged as provisional or completed. Because the scoring construct is different from v1, IPPU/AFOLU scores are **not directly comparable** to the waste/energy/transport scores and should not be pooled into a single cross-sector ranking without a normalisation note.
