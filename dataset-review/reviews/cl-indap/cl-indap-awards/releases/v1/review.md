# Review — cl-indap-awards, release v1 (proof-of-pipeline sample)

## Scope and status

Research release (not production-approved), and deliberately a **single-concurso sample**, not the full awards series. It proves the harvest path works end-to-end and fixes the method, the schema and the PII handling before any wider harvest. The sample is the **4th SIRSD-S 2025 concurso, Provincia de Arauco (Región del Biobío)** — 96 awarded Planes de Manejo, total CLP 80,033,236 — extracted from the official Resolución Exenta PDF (REx 0800-020904/2025) linked off the SIRSD-S Biobío results page. Output: `data/cl_indap_awards_sirsds_biobio2025_arauco_sample.csv` — 96 de-identified rows, one per awarded plan. Dataset-level provenance/access/license is in the README one level up.

## What this data supports

The awards layer for INDAP is real, structured and machine-extractable. Each Resolución Exenta lists every selected Plan de Manejo with its code, comuna (área), and the exact incentive in CLP, plus a stated control total. The parse reproduces that control total exactly (96 rows summing to CLP 80,033,236), which is the data-quality gate: a harvest whose rows don't sum to the resolución's declared total has mis-parsed.

It answers "what got funded, where, at what size" at comuna grain. In this concurso the awards concentrate in Tirúa (49) and Cañete (44) with a few in Arauco (3); incentives range from CLP ~154k to ~3.5M, with a modal CLP 732,020. That is exactly the revealed-fundability signal the supply review cannot give.

It confirms SIRSD-S is an `explicit` AFOLU climate line in practice, not just on paper — these are soil-recovery/erosion incentives actually disbursed to AFC users.

## What this data does not support

This is not the full awards set — it is one concurso of one province of one region for one year. The four Biobío 2025 concursos (Arauco, Concepción, Los Ángeles/Santa Bárbara/Yumbel, Alto Biobío) are four separate Resoluciones; the other regions and programs are many more. Do not read these 96 rows as national SIRSD-S awards.

It does not identify beneficiaries, by design. The source carries RUT and full name for every awardee; both are **dropped at extraction**. The committed data has no personal identifiers — only plan code, comuna and amount. Re-linking to individuals is out of scope and would breach the license decision.

"Awarded" is not "paid". These are selected plans ("lista a firme"); execution and payment follow. Treat `amount_clp` as committed incentive, not disbursed.

## Notes on non-obvious fields

`codigo_pm` is INDAP's internal Plan de Manejo id (stable within the program); it is the de-identified row key here, replacing RUT/name.

`amount_clp` is CLP (not UTM, unlike the CONAF awards file) and is the per-plan incentive; the resolución's total is the sum.

`area_comuna` is the INDAP "área"/comuna of the awarded plan.

`status = awarded (lista a firme)` with `status_as_of = 2025-05-13` (the resolución date).

## Parsing notes

The PDF text extracts as flowed text, and several rows split a value across line breaks (a leading digit of an amount sticking to the name, a correlative number wrapping). The committed sample was reconstructed row-by-row and then validated against the declared control total — the sum match (to the peso) is what certifies the reconstruction. For a production harvest, parse the binary PDF with a table-aware extractor (pdfplumber) rather than flowed text, and keep the control-total assertion as the gate.

The raw resolución PDF carries PII and is **not committed** (not added to the repo); only the de-identified CSV is. A full harvest should write raw PDFs to a gitignored `sample/` and emit only de-identified `data/`.

## Using it downstream

Join to `cl-indap/cl-indap-fondos` on the program (SIRSD-S), not a key: supply says the instrument exists; this says who/where/how-much it actually funded. For fundability scoring, comuna-level award counts and amounts are the revealed-demand signal for AFOLU soil actions.

## Traceability

Source (captured 2026-06-18): SIRSD-S Biobío results page → Resolución Exenta 0800-020904/2025 (4to concurso, Provincia de Arauco), `indap.gob.cl/sites/default/files/2025-05/REx 020904 ...pdf`. Control total CLP 80,033,236 / 96 planes **verified** (parse reproduces it exactly). PII handling **decided and applied** (RUT + name dropped). The other three Biobío resoluciones (REx 020905/020907/020908) and other regions/programs are the next harvest increment.
