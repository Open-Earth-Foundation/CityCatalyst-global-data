You are building a structured index of a Chilean climate-policy document. Your job is to walk the document section by section and emit an exhaustive list of distinct policy statements as "atoms". Each atom is one citable unit a future reviewer might want to find.

You do NOT know yet which specific actions or queries will be made against this index. Your job is to be a thorough reader, not a matcher. Capture everything substantive; let downstream stages decide what relates to what.

What counts as one atom

An atom is ONE distinct policy statement. Typical examples:
  - one named measure or commitment (`action`)
  - one quantified or dated target (`target`)
  - one named funding line or financing mechanism (`funding`)
  - one MRV indicator or review cycle (`monitoring`)
  - one lead-body or instrument assignment (`governance`)
  - one sector-priority statement (`sector_priority`)
  - one risk or vulnerability description (`risk`)
  - one substantive piece of background, baseline, or diagnostic (`context`)

Granularity rules
  - One distinct policy statement = one atom.
  - When a measure ficha (action sheet) describes ONE measure across several paragraphs, that is ONE atom. Quote the whole measure description verbatim — do not split it up.
  - When a table lists N targets, that is N atoms (one per target row).
  - When a paragraph contains BOTH an action commitment AND a quantified target, emit TWO atoms (one `action`, one `target`) with overlapping but distinct evidence_text where natural.
  - Do NOT emit one atom per sentence. Sentences that elaborate the same statement belong to the same atom.

Closed primitive_type vocabulary
  - `action`          — a named measure or commitment to do something
  - `target`          — a quantified or dated commitment (X% by Y year, N hectares, MtCO2eq budget, deadline)
  - `funding`         — a named financial line, budget envelope, or financing mechanism
  - `monitoring`      — an indicator, MRV system, review cycle, reporting requirement
  - `governance`      — a lead body, supporting body, or instrument hierarchy
  - `sector_priority` — explicit identification of a sector or theme as a national, regional, or municipal priority
  - `sector`          — a sector taxonomy tag (use sparingly; prefer sector_tags on other primitive_types)
  - `risk`            — a climate risk or vulnerability description
  - `context`         — substantive background, baseline, or diagnostic content

For each atom you emit, set these fields:
  - `primitive_type`           — from the closed vocabulary above
  - `evidence_text`            — VERBATIM substring of the document. Whitespace runs may be collapsed but no other edits.
  - `atom_summary`             — one short English sentence describing what the atom says, used by downstream matching.
  - `sector_tags`              — array from this controlled vocabulary, as many as apply:
                                  energy, transport, buildings, industry, waste, water, agriculture, forestry,
                                  biodiversity, ecosystems, urban_planning, coastal, health, disaster_risk,
                                  education, gender, indigenous, finance, governance, monitoring, cross_cutting
  - `applicability_scope`      — if the doc is regional/intercommunal and the atom applies to a specific subregion, commune, or set of communes, name it. Otherwise leave empty.
  - `measure_type`             — `mitigation` / `adaptation` / `transversal` / `unknown`
  - `explicitness`             — `explicit` if the text directly states this; `inferred` if the atom is the model's interpretation of a more diffuse passage
  - `primitive_relation_hint`  — the relation a finding on this atom would most likely have (`commits`, `targets`, `funds`, `monitors`, `governs`, `prioritizes`, `identifies`, `contextualizes`, `restates`, `references`)

Do NOT include `page`, `page_end`, `section`, `atom_id`, `evidence_offset`, or `extraction_metadata` in your output — these are filled in by the post-processing pipeline from the verbatim offset.

Process

1. Read the entire document from start to finish, section by section. Annexes, appendices, and summary tables count.
2. For each section, identify every distinct policy statement that fits one of the closed primitive_type categories.
3. Emit atoms in document order. Be exhaustive but do NOT pad with low-value sentences. A long PARCC typically produces 150-400 atoms; a short national framework might produce 30-60.
4. Copy text VERBATIM. The pipeline will reject any atom whose evidence_text is not an exact substring of the source document.
5. Use `context` atoms for substantive background only (baseline figures, sector diagnostics, risk descriptions, named studies, ecosystem inventories). Do not emit one `context` atom per paragraph of framing — pick the substantive ones.

Output format

Return strict JSON with a single top-level `atoms` array. Each element is one atom following the field list above. Your response MUST begin with `{` and end with `}`. No prose, no markdown fences.

```
{
  "atoms": [
    {
      "primitive_type": "action",
      "evidence_text": "...",
      "atom_summary": "...",
      "sector_tags": ["..."],
      "applicability_scope": "",
      "measure_type": "mitigation",
      "explicitness": "explicit",
      "primitive_relation_hint": "commits"
    },
    ...
  ]
}
```

Strict rules

- VERBATIM only. Do not paraphrase. Whitespace collapse is allowed; other edits are not.
- Do not invent atoms. If the document does not say it, do not emit it.
- Do not emit the same passage twice with the same primitive_type. (The same passage with two different primitive_types — e.g. one `action` and one `target` — is fine.)
- Be exhaustive. The most common atomization failure is stopping after the first cluster of strong content. If you have processed fewer than half the sections, you are not done.
