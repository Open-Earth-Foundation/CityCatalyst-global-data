# Extraction Rules · v1

Normative rules for the atom extraction stage. The synthesis stage has
its own per-family rubrics under `v1/rubrics/`. These rules are
extractor-facing and stage-2-only.

## Purpose

To produce an atom layer that is faithful to the source, page-grounded,
and stable across documents. Atoms are the audit substrate; if they are
wrong or paraphrased, every later layer inherits the error.

## Cardinal rules

1. **One atom is one fact.** Do not bundle multiple distinct
   commitments, targets, or actors into a single atom. If a paragraph
   states three measures, it produces three atoms (or more if each
   measure carries its own target or actor).
2. **`evidence_text` is verbatim.** Copy the supporting excerpt
   character-for-character from the page text. Preserve language,
   accents, ligatures, smart quotes, capitalization, and punctuation.
   No paraphrase, no translation, no reformatting beyond a single-space
   whitespace collapse.
3. **`evidence_text` is short.** Prefer one sentence. Two sentences is
   the maximum. If the source idea spans more, split it into multiple
   atoms — each with its own short verbatim quote — rather than copying
   a paragraph into one atom.
4. **Page-grounded.** Every atom carries `page_start`, `page_end`, and
   the verbatim `evidence_text`. The validator confirms the
   normalized evidence appears in the concatenated normalized text of
   pages `[page_start..page_end]` from
   `data/markdown/<source_document_id>/document.md`.
5. **One source document per atom.** Never combine evidence from
   multiple documents into a single atom. Cross-document linking is
   the synthesis stage's job, via `echoes_atom_id`.

## Required fields

Every atom must populate, at minimum:

- `atom_id`
- `source_document_id`
- `primitive_type`
- `evidence_kind`
- `evidence_text`
- `page_start`, `page_end`
- `explicitness`
- `extraction_method`

Atoms missing any of these are rejected before write.

## Primitive types

Use the smallest enum value that fits the fact. The eleven values are
`context`, `risk`, `sector_priority`, `target`, `action`, `actor`,
`timeline`, `funding`, `monitoring`, `governance`. If a single source
sentence carries both an action and a quantified target, produce two
atoms (one of each primitive type) sharing the same evidence span.

## Evidence kind

- `quantitative`: the atom carries a parsed number — populate
  `raw_value_numeric` and `raw_unit`.
- `qualitative`: the atom describes a state, commitment, or framing
  in prose without a parsed number.
- `categorical`: the atom assigns the source to a known category or
  vocabulary (e.g. naming a sector as a priority sector).

## Numeric extraction

When the source carries a number, populate both:

- `raw_value_numeric` — the number as a JSON number, with the
  document's stated scale already applied (e.g. "1.324 billion USD"
  becomes `1324000000` only when the source unit is unambiguous;
  otherwise keep the source's scale and put the unit's modifier in
  `raw_unit`, e.g. `1324` with `raw_unit: "USD millions"`).
- `raw_unit` — a short string (`"MtCO2e"`, `"%"`, `"USD"`,
  `"USD millions"`, `"GWh"`, `"hectáreas"`).

Always also populate `target_value_text` with the verbatim or
near-verbatim source phrasing for the number, so reviewers can audit
the numeric parse against the source language.

## Explicit vs inferred

- `explicit` when the document directly states the fact.
- `inferred` only when the inference is modest and traceable:
  normalizing a named sector to the controlled vocabulary, identifying
  a coastal measure as `territorial_condition: ["coastal"]` when the
  source clearly says coastal, or assigning a measure_type when the
  source's framing is unambiguous.

Unacceptable inference includes assigning a comuna when none is named,
converting a strategic objective into a specific operational action,
or assuming a measure is funded because the plan is official.

## Use `unknown` over guesses

If a field cannot be supported by the cited evidence, omit it (when
the field is optional) or set it to `"unknown"` (when the enum has
that value). Do not guess. The synthesis stage prefers fewer
high-quality atoms over many guessed-at atoms.

## Territorial scope

`region_code` and `communal_code` come from the document registry
unless the cited evidence explicitly names a different scope. Do not
infer city-level applicability from a regional document. Do not add a
comuna to a national document just because the document references the
comuna in passing.

## Section-aware extraction

The atom extractor receives pages already filtered by the section map.
Skip-flagged pages (procurement, legal annexes, abbreviations, table
of contents, gender annex, financial management procedures, etc.) are
not sent to the extractor at all. If the extractor sees a page it
believes was wrongly included, it returns no atoms for that page and
sets the atom-extractor diagnostic note. Do not extract atoms from
pages whose only content is administrative scaffolding.

## Sector vocabulary

Normalized values for the `sector` field. Use the closest match; put
the original source label in `theme` when the source uses a
non-standard term.

Climate sectors: `agua`, `agricultura`, `biodiversidad`,
`bosques_silvicultura`, `borde_costero`, `ciudades_asentamientos`,
`energia`, `infraestructura`, `mineria`, `pesca_acuicultura`, `salud`,
`transporte`, `turismo`, `residuos`, `riesgo_desastres`,
`educacion_cultura`, `multi_sector`.

Environmental quality sectors (PRAS-specific): `calidad_aire`,
`suelo`, `social_comunidad`, `industria`.

If the source uses a sector label outside this vocabulary, set
`sector` to the closest match and put the original Spanish label in
`theme`.

## Restatements

When an atom restates a fact present in a higher-level document
(e.g. a PARCC restates an NDC target), still extract it as a normal
atom of the appropriate primitive_type. Do not flag it as
`echoes_atom_id` at extraction time — that link is established by the
synthesis stage when it has visibility across documents.

Do, however, mark restatements in `notes` with a hint such as
`"restates national framework target"` so the synthesis stage can
prioritize accordingly.

## Don'ts

- Do not turn themes into actions. "Energy transition is a priority"
  is `signal_type: sector_priority`, not `action`.
- Do not overstate readiness. Use `readiness_status: unknown` when
  the document does not clearly indicate the status.
- Do not invent funding certainty. `funding_status: identified` only
  when the document names a specific source, channel, or budget line.
- Do not summarize. Each atom is a single fact, not a synthesized
  observation.
- Do not extract from skip-flagged sections. If the section_map said
  skip, trust it.

## Practical acceptance test

An atom is acceptable only if a reviewer can:

1. open the source document
2. go to the cited page
3. find the verbatim `evidence_text`
4. and confirm the atom's structured fields against that evidence
   in under 30 seconds

If not, revise the atom or drop it.
