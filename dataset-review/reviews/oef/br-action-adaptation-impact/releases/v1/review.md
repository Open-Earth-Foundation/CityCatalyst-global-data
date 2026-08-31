# OEF — Brazil action adaptation impact (br-action-adaptation-impact)

An I Care Brasil workbook that decides which adaptation actions belong to which AdaptaBrasil sector, how strongly each action moves that sector's vulnerability and exposure, and how those judgements become a 0–1 impact score for a municipality. Circulated 26 August 2026 as a working draft; this entry covers that draft.

**Status: research. Do not ingest as an accepted mapping.** The original workbook is partial. The V1 rebuild now covers all six sectors, but its mappings and evidence remain proposed until human review is complete. The implemented method is documented in [`../../methodology.md`](../../methodology.md).

## At a glance

| Measure | Result |
| --- | ---: |
| Sectors in the framework | 6 |
| Sectors with eligibility complete | 3 |
| Sectors with any effectiveness rating | 3 |
| Actions assessed per sector | 53 |
| Possible action × sector × component pairs | 636 |
| Pairs judged eligible | 41 |
| Pairs carrying an effectiveness rating | 31 |
| Verbatim evidence quotes captured | 50 |
| Evidence sources registered | 62 |
| New actions surfaced, in no catalogue | 3 |
| Cities scored | 2 (formula test) |
| Worksheets | 22 |

The 636 figure is the assessment space, not a coverage claim. Roughly 5% of it carries an effectiveness rating and all of that sits in three sectors.

## What the workbook contains

Six sector worksheets share one template and are filled to very different depths. Reading any single sheet without this table gives a false picture of coverage.

| Sector | Eligibility | Effectiveness | Evidence quotes | Sources registered |
| --- | --- | --- | ---: | ---: |
| Water Resources | complete | complete | 40 | 10 |
| Food Security | complete | partial, no citations | 9 | 12 |
| Biodiversity | complete | one row only | 1 | 10 |
| Health | empty | empty | 0 | 10 |
| Energy Security | empty | empty | 0 | 10 |
| Geohydrological Disasters | empty | empty | 0 | 10 |

Water Resources is the only sheet carrying the full workflow and is the reference pattern the cover page names. Every sector's source register is substantially filled with real documents, so the remaining work is assessment rather than sourcing.

## What it gets right

Three properties make the output auditable and are worth preserving through any rebuild.

Judgements are made against **named AdaptaBrasil terminal indicators**, not against themes. Most vulnerability branches end at level 6, but Energy Security vulnerability and all Exposure branches end earlier; the indicator id is therefore authoritative, not a fixed hierarchy depth. Eligibility applies a **primary-mechanism test**, rejecting actions whose link to the sector is a secondary benefit or one narrow example inside a broad action. Every effectiveness rating carries a **verbatim quote with a page reference**, and the High-versus-Medium split follows a consistent stated rule: High when the evidence includes a quantified outcome, Medium when the mechanism is documented but unquantified.

## Interpretation warnings

These are the issues that silently bite downstream use. Each states what must change in handling.

| Issue | Downstream rule |
| --- | --- |
| Eligibility and effectiveness disagree | Water Resources rates 19 actions for effectiveness but judges only 13 eligible. Apply the eligibility gate independently; do not trust a rating's presence as a link. |
| The summary matrix follows effectiveness, not eligibility | Its formula flags a sector link whenever any effectiveness class exists, so it reports links for six actions the same workbook rules ineligible. Recompute from the sector tables. |
| The exposure rule is applied inconsistently between sectors | Water Resources returns zero eligible on exposure from 53 actions while Biodiversity returns five and Food Security four. The rule is not yet written down; treat cross-sector exposure comparisons as unsafe. |
| Scores are ordinal, not magnitudes | Every constant is an author-chosen default with no empirical basis, and the confidence factor was set to 0.75 on every scored row, so it discriminates nothing. Rank with them; never sum, average or present them as effect sizes. |
| Vulnerability and exposure add; hazard is excluded | An action scoring on both components can outrank one strongly effective on a single component. Hazard rows are marked Excluded by design, not by omission. |
| Evidence accumulation only raises ratings | Each new PDF complements rather than replaces, so there is no route for a disconfirming source. At least one rating retains a class its own quote qualifies. |
| Review status is uneven | Water Resources distinguishes rows that had evidence added from rows never assessed. Food Security and Biodiversity mark all 53 rows "Reviewed" with identical boilerplate, which is a bulk stamp. Only the first kind evidences review. |
| Two cities, no coverage | Sobral and Caxias do Sul carry identical scores because city vulnerability and exposure values were never joined. The sheet is a formula test. |
| One definition pair is swapped | In the scaled scoring test, `icare_0145` carries the definition of `c40_0051` and vice versa. Ids and scores are consistent; the pasted definitions are not. |

## Parsing notes

The file is a working environment rather than a data export, and every hazard below follows from that. Two sheets are empty section dividers and two more are superseded copies that still hold plausible-looking data.

| Hazard | Handling |
| --- | --- |
| Prose, prompts and titles surround every table | Read the named Excel tables (`tbl_WR_Assessment`, `tbl_Summary_Linkage`, and so on), never the sheet grid. |
| Row offsets differ by sector | The Water Resources assessment table starts at row 111; the other five start at 118. Address by table name only. |
| The Summary Matrix stacks three unrelated tables | A linkage table at rows 3–56, a parameter table at 60–64, a numeric table at 68–121, all sharing columns. Reading the sheet as one rectangle yields a header row three times over. |
| Both summary tables are formulas | `XLOOKUP` chains over the six sector tables. Cached values may be stale and uncached reads return empty. The sector tables are the source of truth. |
| Controlled vocabularies have drifted | The `Lists` sheet defines review statuses the sheets do not use, and "No effectiveness" is written as "No demonstrated effectiveness". Map values explicitly and fail on anything unmapped. |
| Evidence is newline-delimited inside single cells | Evidence id, source, page and quote each hold parallel newline-separated lists. Split on newline and assert the four lengths match. |
| Page references combine two numbering systems | Entries read "Printed page 629 \| PDF page 79", sometimes with only one present. Neither number alone locates the quote. |
| Action names are unsafe as keys | Names carry non-ASCII hyphens, curly quotes and leading spaces, and sector names switch to Portuguese in the scoring sheets. Join on action id. |
| Three actions resolve against no catalogue | `WR_ADD_0001` to `WR_ADD_0003` are genuinely new. An inner join to the action catalogue silently drops the workbook's only new content. |

## Licence

No licence is stated in the workbook or the covering message [verified by inspection: the cover sheet carries only date, author and version]. The restrictive default applies. This is an unpublished I Care Brasil work product circulated inside the C40 Brazil consortium: internal project use only, no redistribution or publication without I Care's written agreement.

Two input classes keep their own terms regardless. The AdaptaBrasil framework and the three action catalogues keep the licence recorded in their own reviews, and the evidence quotes are short third-party excerpts quotable with attribution but not redistributable in bulk.

## Scope

The unit of assessment is the action, not the place. Every eligibility and effectiveness judgement is a national-level statement about an action-sector pair and none of it varies by municipality. Geography enters only at the final scoring step, where national judgements meet a city's own AdaptaBrasil values.

There is no time series. The evidence base is a fixed portfolio of ten to twelve documents per sector published between 2009 and 2026, and the assessments are a snapshot of August 2026. The workbook is under active revision and will be superseded rather than updated.

## Current release

**v1**, containing the 26 August 2026 source workbook and the proposed all-sector rebuild. Research only; no catalogue entry and no production approval.

The V1 implementation produces a national action-to-risk-component mapping with categorical inputs for a downstream prioritisation index; it does not calculate a city result. Eligibility is indicator-referenced, effectiveness is component-level, and verbatim page-located evidence remains the auditable basis. Human feedback is applied to the V1 inputs before an accepted V1 output can be approved.

### References

- Method and open questions → `../../methodology.md`
- Implementation and rerun instructions → `implementation.md`
- Record contracts → `schemas/`
- Source workbook → `data/Sectoraction_linkage_assessment_V1.xlsx`
- Proposed warehouse mapping → `data/output/action_risk_mapping.csv`
- ICare review workbook → `outputs/icare-review-2026-08-30/icare_adaptation_assessment_review.xlsx`
- Action catalogues → `reviews/c40/c40-high-impact-actions`, `reviews/ipcc/ipcc-climate-actions`, `reviews/icare/icare-climate-actions`
- Sector and indicator framework → `reviews/br-mcti/br-adaptabrasil`
