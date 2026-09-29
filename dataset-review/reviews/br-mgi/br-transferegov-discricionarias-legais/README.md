# Ministério da Gestão e da Inovação em Serviços Públicos — Transferegov transferências discricionárias e legais

This review covers the open-data exports for federal discretionary and legal transfers administered through Transferegov.br. The files connect programmes and proposals to agreements, budget commitments, disbursements, beneficiary payments and status histories. **Status: Steps 1–4, the extraction notebook, proposal-grain working output, draft release review and a bilingual schema pass are complete. Free-text English translation, proposal-level adaptation adjudication, licence resolution and reviewer sign-off remain pending; nothing is production-approved.**

## What this source can establish

Transferegov is not itself a finance pathway; it is the administrative system through which several federal-transfer pathways are recorded. It provides a set of distinct evidence stages:

1. `programa` records the federal programme or offer.
2. `proposta` records an applicant's proposal and requested values.
3. `convenio` records the resulting instrument, including whether it was signed and its current situation.
4. `empenho` records budget commitments, including cancellations and reversals.
5. `desembolso` records transfers from the federal government to the agreement account.
6. `pagamento` records onward payments to beneficiaries or suppliers.
7. `historico_situacao` records the sequence of proposal and agreement states, including approval, rejection, signing and execution.

This distinction addresses the political-continuity question. A programme listing or selected proposal is evidence of political allocation or availability, not secured finance. An `empenho` is a budget reservation and can occur during formalisation before the agreement is signed; it is not a cash transfer and can later be cancelled. A signed agreement establishes formalisation. Disbursement is the strongest signal in these files that federal cash has moved beyond allocation, and payment shows onward use from the instrument account. These stages are not a strictly monotonic ladder: 12,474 instruments in the snapshot have a positive net commitment but are not currently marked signed, while 7,211 disbursed instruments no longer have a positive net commitment after later events.

The stages can support comparisons of historical conversion rates and elapsed times for action categories, but they cannot by themselves prove that one future action is intrinsically easier to finance. The working analytical rules are in [`methodology.md`](methodology.md).

## Canonical access

The current publisher entry point is the Transferegov.br open-data portal operated by the Ministério da Gestão e da Inovação em Serviços Públicos. The complete Discricionárias e Legais source remains available as CSV exports. The publisher began a replacement API rollout in 2026, with financial-execution endpoints scheduled for March–June 2027, so the CSV files are the complete source for this review and the API is a staged successor.

- Open-data portal → https://api-publica.transferegov.gestao.gov.br/
- Discricionárias e Legais download area → https://api-publica.transferegov.gestao.gov.br/downloads
- Official legacy download description and inventory → https://www.gov.br/transferegov/pt-br/ferramentas-gestao/dados-abertos/download-dados
- Official API rollout notice → https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br
- Official API delivery schedule → https://www.gov.br/transferegov/pt-br/comunicados/comunicados-gerais/2026/comunicado-24-2026-cronograma-de-disponibilizacao-da-apis-de-dados-abertos-do-discricionarias-legais
- Direct CSV repository pattern → `https://repositorio.dados.gov.br/seges/detru/{filename}`

The user supplied eight official archives. Profiling showed that `siconv_programa_proposta.csv.zip` is only a bridge table, so the official `siconv_programa.csv.zip` master was also retrieved to make programme names, modalities and budget actions interpretable. The nine CSV archives and publisher data model are stored locally under `releases/2026-07-17/sample/`; this raw sample directory is gitignored.

## Profile of the 17 July 2026 snapshot

All nine CSV files are semicolon-delimited, UTF-8 with BOM, rectangular, and readable as streaming tables. Together they contain about 21 million rows. The snapshot inventory is preserved here because the raw archives are gitignored.

| File | Rows | Columns | Candidate grain / key | SHA-256 |
|---|---:|---:|---|---|
| `siconv_programa.csv.zip` | 1,255,214 | 20 | 52,935 unique `ID_PROGRAMA`; repeated across `UF_PROGRAMA` values | `19c33fc8799e078b60aa2f74fadae5d0a90875dbf0a4946ec91f639041c4ec87` |
| `siconv_programa_proposta.csv.zip` | 1,155,057 | 2 | unique programme–proposal bridge | `9ae6013728a3fb69b81cc75a69d162b501d5d8929d1dfdd0d6ecf170ecf31011` |
| `siconv_proposta.csv.zip` | 1,153,701 | 36 | unique `ID_PROPOSTA` | `55c4dc8ff6fc85a9dc65b8f7e09176794dabf88362aa5143c68e22d7cc69e817` |
| `siconv_convenio.csv.zip` | 285,743 | 40 | unique `NR_CONVENIO` | `7b4d1b9ab5c822184bffae77f993b6e3c8a705f22a2f3d86f7aa4faa5c3e4a34` |
| `siconv_empenho.csv.zip` | 434,899 | 18 | financial events; `ID_EMPENHO` is not globally unique | `9051f2166cffa96bffb08e0668d09e8625284e6eb6d6563a7df0ebaf2a3ea087` |
| `siconv_desembolso.csv.zip` | 378,212 | 11 | unique `ID_DESEMBOLSO` | `5405fa15853aa6d2a0b672f48676d4f98f922323d71575f38f99bf293ddce561` |
| `siconv_pagamento.csv.zip` | 7,359,136 | 11 | unique `NR_MOV_FIN` | `4cfa2b4bffcd27481f0132508861d3d34b495516aacdb06cb722c17b4abaad0d` |
| `siconv_historico_situacao.csv.zip` | 8,957,864 | 6 | status events; candidate event key has duplicates | `288770dc643d655f0ea79081fba77cfa025479a884c25cdedcc175019622d0d5` |
| `modelo_dados_siconv.zip` | 486 archive members | — | publisher SchemaSpy data model | `42d8669748075f6e5387a21267727e64c1a6dcbfea5181b6063574a74dd81e37` |

The relational coverage is unusually strong. All 285,743 agreements link to a proposal. Every nonblank agreement identifier in the commitment, disbursement and payment files resolves to the agreement table. Of 1,155,057 programme–proposal links, all resolve to a programme and only three do not resolve to the proposal snapshot. The status history has 18 proposal identifiers not present in the proposal snapshot; its 3,281,337 blank agreement identifiers are expected for proposal-stage events that occur before an agreement exists.

The proposal table contains municipality, IBGE municipality code, state, applicant legal nature, modality, requested values, an investment-item field and a nearly complete free-text object (`OBJETO_PROPOSTA`, 66 blanks in 1,153,701 rows). These fields make action classification possible, but the source does not provide a ready-made climate or adaptation taxonomy.

## Spatial and temporal scope

The proposal snapshot covers all 27 Brazilian federal units and includes municipal governments, states and the Federal District, public consortia, nonprofit civil-society organisations and public or mixed-capital companies. Municipal government is the dominant applicant class (1,008,381 of 1,153,701 proposals).

Proposal dates run from 1 January 2008 through 16 July 2026, and the latest financial events run through 16 July 2026. The status history contains records as early as 1991, which appear to be migrated legacy history rather than evidence that Transferegov operated in that year; this interpretation remains to be confirmed from publisher methodology.

## License

The publisher describes these products as open data, public, available to all and intended for analysis and reuse. However, no dataset-specific named licence or file-level terms were found at this checkpoint. The CC BY-ND notice in the gov.br site footer governs site content and is not sufficient evidence that the CSV database carries that licence.

Commercial redistribution, attribution wording and treatment of a normalised derivative database remain **unanswered**. The source must not be described as cleared for platform redistribution until an operative licence is identified.

## Interpretation and quality warnings

- `programa` has 1,255,214 rows but only 52,935 unique programme IDs because IDs recur across `UF_PROGRAMA` values; programme rows must not be counted as distinct programmes.
- `empenho` contains cancellations, reversals and 69,715 negative values. `ID_EMPENHO` repeats across agreements and is not a global deduplication key; signed values must be aggregated at agreement grain while retaining event descriptions.
- `pagamento` contains 25,420 zero and 27 negative values. It also contains supplier identifiers and names. Both `IDENTIF_FORNECEDOR` and `NOME_FORNECEDOR` must be dropped at load and must not enter release outputs.
- Several date columns contain impossible years, including years 0001, 0006, 3012 and 5010. Date validation must be field-specific; invalid dates must become null with a quality flag rather than silently parsed.
- The agreement table has 32 negative committed-value records. Sixteen are floating-point residues below one centavo; the other sixteen are genuine negative totals that equal the agreement's own commitment-event net, typically cancellations recorded without the original commitment. The proposal table has two negative counterpart values. Negative amounts are kept and flagged, never repaired.
- Status history includes 18,679 repeated nonblank candidate event keys and 217,770 records with `COD_HISTORICO_SIT = -1`. The `-1` code is not a sentinel for missing data: it marks four labels that have no numeric code (`PRESTACAO_CONTAS_CONCLUIDA`, `PRESTACAO_CONTAS_COMPROVADA_EM_ANALISE`, `RASCUNHO`, `PLANO_TRABALHO_ENVIADO_ANALISE`), so the text label is authoritative. Repeated events do not affect first-event dates but must not be used to count events.
- The agreement table's own committed total (`VL_EMPENHADO_CONV`) differs from the sum of its commitment events for 7,833 agreements, while disbursement events reconcile exactly with `VL_DESEMBOLSADO_CONV` for every agreement. Commitment must be taken from the event file, not from the agreement total.
- Submission events in the status history begin in April 2010. City proposals dated 2008–2009 (about 132,000) have no usable submission event and cannot enter submission cohorts; they stay in the output with `is_submitted = False`.
- Signature and funding run on different clocks. Almost all eventual signatures (99.6%) happen within 12 months of submission, but only 53% of eventual first disbursements arrive within 24 months and 88% within 36 months. Funding comparisons need at least 36 months of follow-up, so cohorts submitted from 2023 onward are not yet comparable for disbursement.
- The share of signed instruments later annulled, rescinded or cancelled falls for recent signing years mainly because cancellations accumulate years after signature. Comparisons around government transitions must hold follow-up time constant.
- Most of the portfolio is not adaptation. By count, submitted city proposals are led by agriculture, tourism and sport programmes, and road paving alone is about a sixth of proposals and R$27 billion of disbursements. A combined programme-and-text screen finds only about 4% of submitted city proposals touching an adaptation theme. Precision varies by theme: water-supply matches are clean, while drainage and disaster-risk matches are noisy because paving and rural-road projects mention drainage and the disaster-prevention programmes also fund roads, bridges and fords. Any adaptation use needs adjudicated matches, not keyword hits.
- Disaster response and recovery transfers, and much Novo PAC drainage and slope work, may sit largely outside this module (inferred, not verified). A missing adaptation record here is weak evidence that no such project was financed.
- Proposal, selection, agreement, commitment, disbursement and payment are different events. They must remain separate; summing across stages would count the same financing multiple times.
- Parliamentary amendments and discretionary allocations recorded in this platform are political allocation mechanisms, not automatically open and repeatable application pathways.
- A proposal is an applicant-authored project request with estimated federal and counterpart resources; its requested value is not an award amount.
- `empenho` means budget reserved for the instrument. It may precede signature and may later be annulled, cancelled or reversed, so it is evidence of commitment at the snapshot date rather than proof that cash is protected from future administrative action.
- `desembolso` is release of the federal share to the instrument account and depends on the instrument schedule and the conceding body's financial availability. It is not the same as expenditure on the adaptation action.
- `pagamento` is a downstream movement to a supplier or beneficiary. It is stronger evidence of financial execution but still does not prove physical completion or effectiveness of the funded action.

## Parsing notes

These are the steps a naive loader gets wrong. Each one is implemented by exactly one block in the extraction notebook, cited by its number.

- **PN1 — text-first load.** Files are semicolon-delimited UTF-8 with BOM. Read every column as text with blanks as null; identifiers such as `ID_PROPOSTA`, `NR_CONVENIO` and IBGE codes are keys, not numbers.
- **PN2 — personal and sensitive data dropped at load.** Never load `IDENTIF_FORNECEDOR` or `NOME_FORNECEDOR` from `pagamento`, or the applicant's address, postcode, district, bank, branch and account columns from `proposta`. The free-text notes on commitments and disbursements are not loaded either. Applicant identifiers are always 14-digit CNPJs, so applicants are organisations.
- **PN3 — amounts in centavos.** Amounts use a decimal comma with no thousands separator, except the unused `VL_SALDO_CONTA`, which uses a decimal point. Some agreement totals carry floating-point residues in scientific notation (for example `-5,82e-11`). Convert to integer centavos before summing, which rounds the residues to zero and makes every sum exact.
- **PN4 — impossible dates.** Dates are `dd/mm/yyyy` (the status history adds a time). Years such as 0010, 0016, 1900, 3012 and 5008 occur. Event dates outside 1 January 2008 to the snapshot date become null and are counted, never guessed.
- **PN5 — programme grain.** `programa` repeats each programme once per state, applicant legal nature and offered modality. Only the modality varies within an ID, so drop it (the proposal carries its own) and keep one row per `ID_PROGRAMA`.
- **PN6 — multi-programme proposals.** 1,231 proposals link to more than one programme and 78 to none. Keep one primary programme (lowest ID) and the programme count, so a proposal is never duplicated in denominators.
- **PN7 — status labels, not codes.** Map `HISTORICO_SIT` labels to stage families (submitted, approved, rejected, signed, annulled or rescinded) and take the first date of each. `COD_HISTORICO_SIT = -1` marks uncoded labels, not missing data.
- **PN8 — city population key.** `COD_MUNIC_IBGE` is a 7-character text key. City applicants are municipal governments and public consortia with a valid code.
- **PN9 — signature.** `IND_ASSINADO = SIM` exactly where `DIA_ASSIN_CONV` is filled, so either identifies signed instruments.
- **PN10 — commitment events.** Aggregate `VALOR_EMPENHO` per agreement using its sign, never the note description (some annulment types carry positive values). `ID_EMPENHO` is not a global key. Four events with a blank agreement number cannot be attributed and are excluded.
- **PN11 — payments back to the recipient.** In `pagamento`, the document type `OBTV PARA O CONVENENTE` (357,195 rows, about R$11.3 billion) moves money from the instrument account to the recipient itself, not onward to a supplier or creditor. Keep it in a separate amount. Zero-value rows carry no movement; negative rows stay in the net.

## Extraction notebook

The release notebook turns the nine files into one proposal-grain table: one row per proposal with its programme, recipient, instrument, first date of each stage, and each stage's amount in its own column. It asserts the profiled row counts, key integrity, the absence of personal-data columns, the named stage-order exceptions, and exact reconciliation of stage totals with the raw files. The notebook also holds the fit cells: stage conversion by submission cohort, time between stages, must-have field coverage, signed-instrument outcomes by signing year and the Novo PAC tracing test. A content section profiles what the proposals are for: the ministry mix, a first-pass adaptation theme screen with a precision sample, and benchmark values for funded agreements by theme.

The output table has about 1.15 million rows and is too large to commit, so it is written to `sample/` (gitignored) and regenerated by re-running the notebook. The notebook needs about 6 GB of memory at peak and runs in about four minutes. Re-downloads from the publisher are live exports, so they will not match this snapshot's hashes or pinned counts; the validation block will flag that.

References: `releases/2026-07-17/transferegov_extract_fit.ipynb`; output `releases/2026-07-17/sample/br_transferegov_proposals_2026-07-17.csv.gz`.

## Fit for purpose (proposed)

Scored against the finance-pathways need, the proposed verdict is **conditional fit for tracing federal transfers, weak fit for adaptation evidence**. The source meets every must-have field and is the only reviewed source that follows a city proposal through signature to cash, with dates and amounts at each stage. Two conditions hold it back: no operative licence has been found for the CSV files, so records cannot yet be displayed in the product, and only about 4% of city proposals touch an adaptation theme, with no adaptation tag from the source. The verdict awaits reviewer sign-off.

| Criterion | Result | Evidence |
|---|---|---|
| Native record ID | Pass | Proposal and agreement numbers as issued; every join resolves |
| Recipient name and type | Pass | 100% of submitted city proposals; applicants are organisations (CNPJ only) |
| Recipient geography | Pass | UF and 7-digit IBGE code on every proposal |
| Funder or programme | Pass | Programme, ministry and budget action on all but 78 proposals |
| Instrument | Pass | Modality on every proposal |
| Amount with meaning | Pass | Requested, agreed, committed, disbursed and paid kept as separate nominal BRL fields |
| Stage and date | Pass, with a gap | Submission events only from April 2010 |
| Project description | Pass | Object text on all but 66 proposals |
| Disbursement or payment | Pass | Both present; disbursement reconciles exactly with agreement totals |
| Adaptation relevance stated by source | Fail | No source tag; about 4% of city proposals match an adaptation theme screen |
| Links to other sources | Conditional | CNPJ and IBGE codes join to other registries; no shared ID with COFIEX, SADIPEM or Novo PAC lists tested |
| Licence | Unresolved | Open-data statements only; no dataset-specific licence |
| Access | Pass | Bulk CSV without login |
| Temporal coverage | Pass | 2008–2026; cohorts comparable for funding only up to about 2022 |

## Step 3 conclusion

The source is technically and methodologically strong enough for a historical finance-pathway analysis. The primary manuals confirm what proposals, commitments, disbursements and OBTV payments represent, and the working methodology now defines comparable outcome and timing measures. The data still cannot support a causal claim that an action type itself caused easier financing; results must be framed as observed historical conversion and timing conditional on programme, year, geography, recipient type and instrument type.

## Current approved release

No release is approved. The 2026-07-17 release has its extraction notebook and a draft review.md; the proposed fit verdict above awaits reviewer sign-off, and the licence must be resolved before any product use.
