# Review — Novo PAC drainage and slope-containment selections, release 2025-09

## Scope and status

This research release contains 315 proposal observations and three national control totals, a cleaned bilingual table, restartable build notebook and draft adaptation crosswalk. All 279 distinct Portuguese project descriptions now have reviewed English counterparts, while the Portuguese source text remains authoritative. The source-page no-derivatives issue is unresolved. It is not production-approved. The cleaned table and crosswalk are not committed while the no-derivatives question is open. They are written to this release's `sample/` folder; run `build_release.py` to regenerate them from the source extract held in the same folder.

## What this data supports

“Novo PAC selected the published drainage or slope-containment proposal in September 2025 at the stated amount and through the stated OGU or FGTS channel” is supported for the 315 proposal rows. The rows reconcile to about R$10.303 billion for drainage and R$1.432 billion for slope containment, consistent with the published R$11.7 billion control.

## What this data does not support

Selection is not a signed agreement, loan contract, disbursement or completed work. Repeated proposal identifiers cannot be called co-financing or added until a final decision source resolves their relationship. The three controls are not individual projects.

## Using it downstream

Exclude aggregate rows from project metrics. Preserve `native_record_id`, instrument and source list. Use Transferegov to trace OGU proposals toward agreements and payments, and the MCidades investment portfolio or SADIPEM to trace credit proposals toward contracts or later credit stages.

Use `project_description` for English display and retain `project_description_pt` for audit. Proper place names and the consortium legal name are intentionally preserved rather than translated. The row-level status distinguishes exact reviewed translations from reviewed template translations, and source titles and notes carry separate status fields.

## Benchmark values a city can use

The 315 proposal amounts range from about R$0.54 million to R$215.86 million, with a median of about R$22.71 million. These are selected proposal amounts from one programme cycle, not general construction unit costs or guaranteed available finance.

## Traceability

Drainage records map directly to `c40_0048`; slope-containment records map directly to `icare_0184`. Amounts remain on proposals and are never divided across actions. Medium links, if added later, require human adjudication.

The restartable build validates 318 rows, 318 unique record identifiers, 279 distinct Portuguese descriptions, 279 distinct English descriptions, and complete English/Portuguese pairs for project descriptions, source titles and notes. Translation completion left the action crosswalk byte-for-byte unchanged at SHA-256 `3506dae8ba5de44ee4be7718fd1825513b88644a46493a400e347e08b695496f`.
