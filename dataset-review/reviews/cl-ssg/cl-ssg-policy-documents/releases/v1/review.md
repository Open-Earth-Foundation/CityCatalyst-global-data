# Review

## Summary

This release is a curated inventory of Chilean climate and territorial policy documents intended to support policy signal extraction, legal-context indexing, and later mapping from plans to actions. It is not a single-source publisher dataset. Instead, it is a manifest of links and placeholders spanning national, regional, communal, and inter-communal planning instruments.

The intended end use is not just document cataloguing. The main goal is to assess, for each Chilean city, which actions align most closely with the policy environment that applies to that city, and to express that alignment as a strength score backed by extracted evidence from the relevant policy documents.

The core climate-planning logic is a nested stack:

> NDC -> ECLP + LMCC -> Sector Plans -> PARCC -> PACCC

Each layer makes the one above it more concrete and more local:

- Frameworks set long-term goals, obligations, and scope.
- Instruments turn those goals into actions, plans, programs, financing pathways, and monitoring structures.

For review and signal extraction, the most useful practical order is:

> PACCC -> PARCC -> Sector Plans -> national frameworks

This reflects where implementation detail is most likely to appear. Municipal and regional documents are the strongest candidates for extractable actions, delivery actors, funding pathways, timelines, and monitoring commitments. National frameworks are still important, but mainly as alignment context unless they include explicit measures or targets.

## Intended use case

The core use case for this dataset is city-level action-to-policy alignment.

In practice, that means:

1. Identify the policy documents that apply to a given Chilean city.
2. Extract evidence from those documents, such as sectors, measures, targets, delivery actors, timelines, and funding mechanisms.
3. Compare that evidence against a library of candidate actions.
4. Score how strongly each action aligns with the applicable policy environment for that city.

The desired output is not simply "does this action appear in a plan." It is a more nuanced evidence-backed alignment judgement, for example:

- strong alignment where a local or regional policy explicitly names the action or an equivalent measure
- medium alignment where the action clearly supports a stated sector priority, target, or implementation pathway
- weak alignment where the relationship is plausible but indirect, generic, or only supported by higher-level frameworks

This also implies an evidence hierarchy. Signals from more local instruments should usually carry more weight than signals from high-level national frameworks:

> PACCC > PARCC > Sector Plans > ECLP / NDC

That weighting reflects intended implementability. A city action that is explicitly present in a municipal or regional plan should usually score as more strongly aligned than an action supported only by a broad national commitment.

## What is in this release

The original curated manifest contained 42 rows. It is supplemented by 14 final municipal climate-action plans from `data/registry/policy_documents_test.xlsx`, bringing the operational source registry to 56 records. The added plans are for Santiago, Providencia, Maipú, Renca, Quilicura, Peñalolén, Valparaíso, Concepción, Temuco, Valdivia, Paillaco, Lago Ranco, Panguipulli, and Frutillar; shared regional plans were reused rather than reprocessed.

The original 42-row manifest contains:

- 12 national records
- 20 regional records
- 8 communal records
- 2 inter-communal records

By policy type, the manifest includes:

- 25 `Climate Change Instruments`
- 13 `Territorial planning instruments`
- 4 `Envirnomental Policy` records

The strongest climate-policy coverage in the current manifest is at national and regional level. In practice this means:

- National frameworks and sector plans are well represented.
- Regional climate action plans (PARCCs) are broadly represented, with one row per region in most cases.
- Municipal climate action plans (PACCCs) are not yet systematically represented in the manifest.
- The communal layer currently contains mostly PRAS records and generic territorial-planning placeholders rather than a broad, resolved PACCC inventory.

## Big-picture policy structure

The older research notes are directionally consistent with the structure implied by this manifest:

| Document family | Level | Role in the stack | Review value |
| --- | --- | --- | --- |
| NDC | National | International/national commitment layer | High for top-level targets and framing |
| ECLP | National | Long-term strategy to 2050 | High for pathways, sectors, and strategic targets |
| LMCC | National | Legal framework creating mandatory instruments and governance | High for legal basis and instrument hierarchy |
| Sector plans | National | Implementation instruments by sector | Very high for concrete national measures and sector targets |
| PARCC | Regional | Regional delivery layer | Very high for subnational actions, financing, timelines, actors, MRV |
| PACCC | Municipal | Local delivery layer | Highest value where available for place-based actions and implementers |

## Notes on PARCCs

A PARCC is best understood as the regional delivery layer that translates national climate goals into region-specific implementation. For extraction purposes, a good PARCC usually contains some version of:

- climate context and risks
- emissions baseline and scenarios
- priority sectors
- mitigation and adaptation measures
- concrete actions
- targets and timelines
- implementing actors
- financing pathways
- monitoring, reporting, and verification

That makes PARCCs especially useful for policy signals such as:

- sector prioritization
- named measures or intervention themes
- quantified targets
- implementation timelines
- responsible institutions
- funding or budget channels
- monitoring commitments

The manifest includes 16 regional climate action plan rows, corresponding to Chile’s regional PARCC landscape. However, the quality and maturity of those rows is mixed:

- Some rows point to final PDFs.
- Some rows point to draft or consultation documents.
- Some rows point to portals, flipbooks, or non-final resources.
- At least one row uses placeholder text rather than a resolvable source URL.

This means regional coverage is broad, but document readiness is uneven.

### Municipal PACCC update

The 14 added municipal plans provide city-specific action evidence in this release for the listed communes. Rows marked `Not ready (In process)` in the supplied workbook were not added. Antofagasta was also not added despite the workbook note to download it: the municipality's published material confirms that its PACCC remains under development, so there is no final plan to ingest. Valparaíso's municipal PACCC is included, while its regional PARCC remains a placeholder.

## Notes on PACCCs

The background notes suggest that PACCCs are sparse, unevenly published, and hard to discover through a central registry. That aligns with the current release: PACCCs are important for local action extraction, but they are not yet systematically present in the manifest.

This is a key gap for downstream work. If the goal is strong action-level mapping, municipal PACCC discovery and curation would materially improve the dataset. For now:

- treat PACCCs as high-value follow-on enrichment rather than a strong current asset of this release
- use PARCCs as the main subnational action source where municipal plans are missing
- use national sector plans for backfilling sector logic, terminology, and target alignment

## Most useful source classes for action mapping

For the current manifest, the best signal-extraction priority is:

1. Regional PARCC documents
2. National sector mitigation plans
3. National frameworks such as ECLP and NDC
4. Resolved communal plans where they contain climate actions
5. Territorial planning instruments as contextual rather than primary action sources

This ranking balances two things:

- likelihood that a document contains explicit actions, targets, actors, and monitoring fields
- likelihood that the document is actually represented in the manifest with a usable source link

For the intended scoring use case, it also reflects expected evidentiary strength. In general:

- PACCC evidence should be strongest for a specific city where available
- PARCC evidence should be strong for cities within that region
- sector-plan evidence should be strong when the action belongs to the covered sector
- national framework evidence should usually act as supporting context rather than decisive proof of alignment

## Expected signal types

The example mapping structure from the earlier notes is a good fit for this dataset. The most natural extractable signal families are:

- `sector`
- `action`
- `target`
- `timeline`
- `actor`
- `funding`
- `governance`
- `monitoring`
- `risk` or `hazard`

For this release, a practical extraction rule is:

- Extract directly stated signals first.
- Only infer action-to-target or action-to-funding links when the document provides a plausible textual basis.
- Keep inferred links separate from explicit signals.

For alignment scoring, it will also be useful to capture a small amount of structured evidence metadata with each extracted signal:

- `evidence_text` or quotation snippet
- `evidence_type` such as `explicit_action`, `sector_priority`, `target`, `funding_reference`, `governance_reference`
- `source_level` such as `municipal`, `regional`, `national_sector`, `national_framework`
- `applicability_scope` indicating which city or territory the signal applies to
- `explicitness` such as `explicit` or `inferred`

## Action mapping model

The proposed structure of `Actions`, `PolicySignals`, and an `Action <-> PolicySignal` bridge is sensible for this review. It supports both direct extraction and later similarity-based linking.

Suggested interpretation:

| Table | Purpose |
| --- | --- |
| `Actions` | Normalized intervention library, deduplicated across documents |
| `PolicySignals` | Raw or lightly normalized evidence extracted from a specific source |
| `ActionPolicySignalMap` | Evidence-backed relation between a signal and a canonical action |

Recommended relation types:

- `supports`
- `prioritizes`
- `targets`
- `funds`
- `implements`
- `monitors`
- `governs`

This structure should support a final city-specific scoring layer, for example:

| Layer | Purpose |
| --- | --- |
| `CityApplicablePolicies` | Resolves which policy documents apply to each city |
| `PolicySignals` | Stores extracted evidence from those applicable documents |
| `ActionPolicySignalMap` | Links evidence to canonical actions |
| `CityActionAlignmentScore` | Aggregates evidence into a city-specific alignment strength |

At a minimum, the final score should consider:

- source proximity: municipal > regional > national
- evidence explicitness: explicit action mention > indirect thematic support
- evidence specificity: named action > sector theme > broad framework
- multiplicity: repeated support across several applicable documents
- consistency: whether signals reinforce each other or conflict

## Review judgement

### Strengths

- Strong conceptual fit for policy signal extraction
- Good spread across national and regional climate-policy instruments
- Explicit territorial coding supports joins and downstream expansion
- Includes both climate instruments and planning context documents
- Suitable as a starting manifest for manual or semi-automated document review

### Weaknesses

- Municipal climate action coverage is currently thin
- Many records are placeholders, draft links, or portal links rather than stable final documents
- The dataset mixes authoritative source links with unresolved inventory placeholders
- `Type of Policy` values are broad and do not yet distinguish framework vs implementation instrument cleanly
- The source is a curated inventory, so consistency depends on manual maintenance

### Overall assessment

This is a high-value review dataset for discovering and structuring Chilean climate-policy signals, especially at national and regional level. It is not yet a complete operational inventory of local climate action plans. For action extraction today, PARCCs and sector plans are the clearest starting point. For stronger locality and implementation detail, PACCC discovery remains the main enrichment opportunity.

It is especially well suited to building a policy-evidence layer that can later be turned into city-level action alignment scores. The main current limitation is not the concept, but the uneven availability of resolved local documents.

## Recommended next steps

1. Classify each row into a tighter policy hierarchy such as `framework`, `sector_plan`, `regional_action_plan`, `municipal_action_plan`, `territorial_planning`, `environmental_recovery`.
2. Add a `document_status` field such as `final`, `draft`, `consultation`, `portal_only`, `placeholder`, `in_process`.
3. Add a `source_kind` field such as `pdf`, `html_page`, `portal`, `flipbook`, `placeholder`.
4. Resolve PACCCs into explicit rows where possible rather than leaving the municipal layer mostly implicit.
5. Prioritize extraction pipelines for PARCC and sector-plan PDFs first.
6. Keep confidence scoring simple at first, with explicit vs inferred distinctions, before introducing vector-similarity scoring.
7. Add a formal scoring rubric for city-action alignment so that evidence extraction and scoring logic are designed together rather than separately.
