# Ministério das Cidades — Novo PAC drainage and slope-containment selections

This review covers the 2025 Novo PAC selection lists for urban drainage and slope containment published by the Ministério das Cidades as five spreadsheets, plus three national control totals from the federal announcement. The working release contains 315 proposal observations and three aggregate controls. **Status: source files, cleaned bilingual release, validation and draft adaptation mapping are complete; legal review of the no-derivatives notice and mapping adjudication remain pending. Nothing is production-approved.**

## Canonical downloads

The canonical proposal-level source is the ministry’s public selection page and its five XLSX files: drainage and slope containment split between OGU transfers and FGTS financing, plus drainage proposals routed from OGU to financing. These files are the source actually used for the working release **(verified)**. The federal announcement supplies the R$11.7 billion, 235-municipality and 26-state controls **(verified)**.

The preferred rights-clear alternative is the corresponding Diário Oficial portarias. Official acts are outside copyright protection under Lei 9.610 article 8 IV **(inferred application; legal confirmation pending)**. The DOU acts should replace the proposal spreadsheets if their annexes reproduce every record and amount; the national announcement may still be needed for control totals.

## License

The ministry page carries the gov.br CC BY-ND 3.0 footer, while the five spreadsheets contain no file-level licence **(verified)**. Commercial use with attribution is permitted by BY-ND, but whether extracting, translating and normalising the tables creates a prohibited adaptation remains unresolved. Until legal review, row-level redistribution is `review`, not clear.

## Spatial and temporal scope

The proposal observations cover 26 UFs and 230 normalized source spellings for beneficiary municipalities. The source announces 235 municipalities; the difference is consistent with repeated and inconsistent names rather than missing proposal rows. All records describe the September 2025 selection stage, not agreements, contracts, disbursements or completed works.

## Interpretation warnings

Twenty-eight proposal identifiers occur in two lists. They may be alternatives, revisions or complementary financing and must not be summed or merged without a final decision source. The three national controls are not projects and must be excluded from project counts and project-value sums.

Selection does not establish formalisation or payment. OGU is a non-reimbursable transfer channel; FGTS is domestic credit. Both can appear under the same programme, so programme and instrument must remain separate.

## Parsing notes

The release table uses English field names and retains all 279 distinct Portuguese project descriptions in `project_description_pt`. Their reviewed English counterparts are complete in `project_description`: 25 rows use exact reviewed translations, 291 rows use reviewed templates that preserve place names, and 2 rows preserve a consortium's proper legal name. The two source-title values and all structured source notes are also paired in English and Portuguese with their own translation status. Native proposal identifiers are extracted from the source notes. Proper place and legal names are not translated, and every row records that treatment explicitly.

The restartable build fails if a previously unseen project description, source title or note pattern lacks a reviewed translation rule. It asserts 318 rows, 279 distinct Portuguese and English project descriptions, complete bilingual pairs and unique record identifiers. The action mapping continues to use Portuguese source text; completing translations does not change its rows or classifications.

## Current approved release

No release is approved. Working release: **2025-09**.
