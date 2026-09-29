# Working methodology — Transferegov finance-pathway evidence

This working methodology translates the Transferegov administrative lifecycle into measures suitable for comparing historical financing outcomes for municipal adaptation actions. It is intentionally narrower than a general evaluation of Brazilian intergovernmental finance. **Status: Step 3 complete and the rules tested end to end by the extraction notebook; they remain working until the fit verdict and review.md are written.**

## What the records measure

The proposal is a request authored by a prospective recipient after a federal body makes a programme available. The publisher requires it to describe the project, explain its relationship to programme objectives, estimate the federal transfer and counterpart contributions, and state the expected execution period. Proposal value is therefore requested or anticipated finance, not an awarded amount. **Verified.**

An `empenho` is the reservation of budget for an approved proposal or work plan as part of formalising an instrument. The publisher's formalisation guidance places this reservation before celebration of a transfer contract, and the data contain annulments, cancellations, reinforcements and reversals. It is a meaningful dedicated-amount signal, but it is neither cash nor irrevocable. **Verified.**

A disbursement is the release of the federal share through a Documento Hábil and Ordem de Pagamento. The publisher states that release follows the instrument schedule and applicable law and remains conditional on the conceding body's financial availability. In the export, `VL_DESEMBOLSADO` is therefore cash released to the instrument, not an announcement and not yet supplier expenditure. **Verified.**

An OBTV supplier payment is a bank transfer from the instrument's resources to a creditor or supplier. Other OBTV types can move money to the recipient itself, pay taxes, place funds in savings or return funds. The supplied `pagamento` export contains only two beneficiary-payment labels, but its type must still be retained when aggregating values. Payment is evidence of downstream financial execution, not proof of physical completion or climate effectiveness. **Verified.**

The status history records administrative states, not a controlled evaluation outcome. Approval, rejection, signature, execution and accountability states can establish observed transitions and timing, but differences between action classes may also reflect programme rules, applicant capacity, project quality, geography, year, instrument modality and incomplete follow-up. **Inferred from the verified workflow and fields.**

## Analytical population and denominator

The primary comparison unit is one `ID_PROPOSTA`. The full bridge contains 1,153,626 distinct proposal identifiers: 78 proposals lack a programme link, three linked identifiers are absent from the proposal snapshot, and 1,231 proposals link to more than one programme. A proposal may therefore carry multiple programme relationships without being duplicated in outcome denominators. **Verified.**

The city-finance population is restricted to proposals whose applicant is a municipal government or public consortium and that have a valid municipality/IBGE location. Other recipient classes remain available as comparison groups but are not mixed into the main city denominator. **Working analytical choice.**

An application cohort requires evidence that the proposal was submitted for analysis, using the first valid `PROPOSTA_ENVIADA_ANALISE` or equivalent complemented-submission event. Draft and merely registered proposals are not applications because the applicant may never have submitted them. Migrated records with no usable submission event remain in a separate coverage table and are excluded from time-to-event estimates. **Working analytical choice grounded in verified status labels.**

Comparisons use submission-year cohorts and must allow a common follow-up window. Recent applications that have not had the same opportunity to reach signature, disbursement or payment are right-censored rather than counted as failures. The extraction notebook settles the minimum follow-up window. In the fully observed 2015–2019 city cohorts, 99.6% of eventual signatures happen within 12 months of submission, but only 53% of eventual first disbursements arrive within 24 months and 88% within 36 months. Signature comparisons therefore use a 12-month window and funding comparisons a 36-month window. Submission events only exist from April 2010, so 2008–2009 proposals stay in the coverage table. **Verified from the snapshot; window choice is a working rule.**

## Financial and administrative signals

| Signal | Operational definition | What may be claimed | What may not be claimed |
|---|---|---|---|
| Programme available | Programme was available for the applicant's state and receipt window | An eligible federal route existed | Money was allocated to a city |
| Proposal submitted | First qualifying submitted-for-analysis history event | The applicant attempted to use the route | The project was selected or funded |
| Approved | First proposal/work-plan approval event, reported by approval family | The proposal passed the recorded review stage | An agreement was signed or money secured |
| Signed | Agreement exists and `IND_ASSINADO = SIM`, corroborated by a valid signature date or `ASSINADA` event where available | A formal instrument was executed | Funds were necessarily disbursed or spent |
| Ever committed | At least one positive `VALOR_EMPENHO` event | Budget was reserved at some point | The reservation remains available |
| Net committed at snapshot | Signed sum of all valid commitment-event values for the agreement is greater than zero | A positive net budget reservation remains in the export snapshot | Cash was transferred or the commitment cannot later be cancelled |
| Disbursed | Signed sum of valid `VL_DESEMBOLSADO` events is greater than zero | Federal resources were released to the instrument | Suppliers were paid or the action was completed |
| Paid | Signed sum of valid `VL_PAGO` events, excluding `OBTV PARA O CONVENENTE` transfers back to the recipient, is greater than zero | Resources moved onward from the instrument account | Physical delivery or adaptation effectiveness occurred |
| Accounted | Terminal accountability event, reported separately for approved, approved with reservations, rejected and concluded | The recorded accountability process reached the named state | All project objectives were achieved |

These signals are not forced into a single ordinal score. In the snapshot, counted in exact centavos, 12,474 instruments have a positive net commitment but are not currently marked signed, consistent with commitment activity during formalisation; all instruments with disbursement or payment are marked signed. There are also 7,211 disbursed instruments with no positive net commitment at the snapshot and 246 instruments with positive onward payments but no positive disbursement in the supplied export. Earlier float-based counts (12,511, 7,210 and 251) treated rounding residues as positive nets and counted payments back to the recipient as onward payments. Those exceptions are retained and flagged instead of repaired into an assumed order. **Verified.**

## Amount rules

All source amounts are treated as nominal Brazilian reais because the exports provide no price basis or real-value series. Cross-year amount comparisons require an external Brazilian deflator and a declared base year; until one is selected, amount results are reported within year or as nominal values. **Verified for source units; deflator choice unanswered.**

Requested federal transfer, counterpart and global proposal values remain separate. Agreement value, net commitment, disbursement and payment remain separate measures and are never added together because they are stages of the same financing rather than independent sources. **Working analytical rule.**

Commitment events are aggregated by agreement using the signed numeric value in `VALOR_EMPENHO`; the event description is retained for audit. The agreement table's own committed total disagrees with the event sum for 7,833 agreements, so it is not used; disbursement events, by contrast, reconcile exactly with the agreement's disbursed total. Negative event values reduce the net and positive event values increase it, without inferring the sign from the description alone. `ID_EMPENHO` is not a global event key and must not be used to deduplicate across agreements. Exact duplicate full rows were not found in the snapshot. **Verified.**

Zero and negative disbursement or payment totals are not treated as successful finance. Negative payment rows remain in net totals and receive a reversal/refund quality flag. Aggregate results report both gross positive movement and signed net movement so reversals remain visible. **Working analytical rule.**

## Action classification

Action classification uses the proposal object as the primary evidence, supported by investment item, programme name, budget action and programme subtype. No single keyword is sufficient. Programme names identify the funding context but cannot automatically assign every linked proposal to the same adaptation action. **Working analytical rule.**

Each proposal can link to zero, one or multiple action classes. Values stay at proposal or instrument grain and are not divided among mapped actions. Multi-action records contribute to a clearly labelled multi-action group or to link-level counts that exclude monetary summation across actions. Uncertain and non-climate proposals remain in the output with `mapping_confidence = none`; they are not silently discarded. **Working analytical rule.**

A first-pass theme screen in the extraction notebook combines object text with programme names and flags about 4% of submitted city proposals as touching an adaptation theme. A read of eight sampled matches per theme puts water supply near-clean, slope and flood at about five in eight, and drainage and disaster risk at about three in eight. The screen produces candidates for adjudication only. **Inferred.**

The target adaptation-action taxonomy and adjudication rules are **unanswered**. They must be aligned with the action-prioritisation work before the extraction notebook produces comparative results.

## Measures for “easier to finance”

No single measure is labelled ease of finance. The analysis reports a panel of outcomes by action class:

- submission-to-approval conversion within a common follow-up window;
- submission-to-signature conversion and median elapsed time;
- signature-to-first-disbursement conversion and elapsed time;
- proportion with positive net commitment at the snapshot;
- disbursed-to-agreement and paid-to-disbursed ratios, both winsorised only for display and never silently altered in source outputs;
- cancellation, annulment, rescission and rejection rates;
- share of requested federal transfer ultimately disbursed, where proposal and agreement values can be reconciled.

Results are stratified at minimum by submission year, state, applicant legal nature, instrument modality and programme. Raw pooled rankings are descriptive and must not be presented as causal evidence that an action type determines financeability. **Working analytical rule.**

Government-transition analysis uses event dates to compare cohorts around a transition, but a change in conversion or timing is only an association unless a defined counterfactual and sensitivity analysis are added. The most defensible resilience indicators are the share of instruments already disbursed before the transition, subsequent cancellation/rescission rates, and time to the next execution stage. **Inferred; causal design unanswered.**

## Known uncertainty and exclusions

Impossible dates are set to null with a field-level quality flag. Status-history dates before the SICONV start in 2008 are retained as migrated legacy records but excluded from elapsed-time calculations unless publisher documentation confirms their semantics. **Working rule; migration interpretation inferred.**

Supplier identifier and supplier name are dropped immediately on load. No person-level or supplier-level analysis is permitted. **Verified data risk and binding processing rule.**

Physical completion, service quality, beneficiaries reached, avoided losses and climate outcomes are outside the supplied files. The data can show administrative and financial execution, not whether an adaptation intervention worked. **Verified from the supplied schema.**

## Primary references

- [Transferegov proposal tutorial](https://www.gov.br/transferegov/pt-br/manuais/transferegov/discricionarias/atos-preparatorios/2-tutorial_dados-da-proposta_convenios_convenente.pdf/@@display-file/file)
- [Transferegov formalisation tutorial](https://www.gov.br/transferegov/pt-br/manuais/transferegov/discricionarias/atos-preparatorios/11-tutorial_formalizacao_convenios_concedente.pdf/@@display-file/file)
- [Transferegov resource-release tutorial: Documento Hábil](https://www.gov.br/transferegov/pt-br/manuais/transferegov/discricionarias/execucao/5-tutorial_liberacao-de-recursos-de-repasse_documento-habil__convenios_concedente.pdf/@@display-file/file)
- [Transferegov resource-release tutorial: Ordem de Pagamento](https://www.gov.br/transferegov/pt-br/manuais/transferegov/discricionarias/execucao/6-tutorial_liberacao-do-repasse-ordem-de-pagamento_convenios_concedente.pdf/@@display-file/file)
- [Transferegov OBTV supplier-payment tutorial](https://www.gov.br/transferegov/pt-br/manuais/transferegov/discricionarias/execucao/9-tutorial_pagamento-de-fonecedores-por-meio-de-obtv_convenios_convenente.pdf/@@display-file/file)
- [Transferegov open-data inventory and data-model instructions](https://www.gov.br/transferegov/pt-br/ferramentas-gestao/dados-abertos/download-dados)
- [Transferegov system history and scope](https://www.gov.br/transferegov/pt-br/sobre/transferegov)
