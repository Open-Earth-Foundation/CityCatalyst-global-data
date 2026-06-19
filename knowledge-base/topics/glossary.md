# Glossary

Simple, shared glossary for terms used across CityCatalyst datasets, models, and reviews.

## How to use this file

- Add terms in alphabetical order under the correct letter section.
- Keep definitions to one sentence in plain language.
- Use `snake_case` for term headings.
- Use comma-separated domain tags in **Domain**.
- Add **Also called** only when useful.
- Add one short, concrete **Example**.

## Entry template

### term_name
- **Definition:** One-sentence definition.
- **Domain:** domain_a, domain_b
- **Why it matters:** Why the term is important in practice.
- **Also called:** optional synonym
- **Example:** One short example.

## A

### activity_data
- **Definition:** Measured or estimated activity amount used as an input to emissions calculations.
- **Domain:** emissions, inventory, methodology
- **Why it matters:** Emissions are often computed from activity data multiplied by an emissions factor.
- **Also called:** activity value
- **Example:** "Diesel bus activity data is 1,200,000 vehicle-km in 2024."

### activity_shift
- **Definition:** Informal synonym for a transition element that emphasizes a change in system state rather than a policy instrument.
- **Domain:** tef, hiap, mitigation
- **Why it matters:** It prevents confusion between interventions as modeled outcomes and policy actions used to achieve them.
- **Also called:** transition element, outcome (in some HIAP docs)
- **Example:** "Shift from diesel buses to electric buses is an activity shift."

### actor_id
- **Definition:** Primary city identifier based on UN/LOCODE used across modelled datasets.
- **Domain:** data-model, city-identity, emissions
- **Why it matters:** It is the reliable join key for city-level data and should be used instead of `city_id`.
- **Also called:** locode
- **Example:** "`BR SAO` identifies Sao Paulo in modelled tables."

### award
- **Definition:** A proposal selected for funding in a given call; an award is not the same as money disbursed.
- **Domain:** finance, awards
- **Why it matters:** Awards data reveals what actually gets funded (revealed fundability), distinct from what funding merely exists (supply). See `topics/data-sources/cl-climate-finance.md`.
- **Also called:** adjudicación, proyecto adjudicado
- **Example:** "CONAF awarded 806 native-forest projects in the 2025 first call."

## B

### bonificacion
- **Definition:** A reimbursement-style grant where the state pays an eligible cost after the work is done, common in Chilean forestry/agriculture funds.
- **Domain:** finance, instruments
- **Why it matters:** It is a grant `instrument_type`, but disbursement is conditional on execution — awarded ≠ paid.
- **Also called:** bono (when paid)
- **Example:** "The Ley 20.283 fund pays a per-hectare bonificación in UTM."

## C

### call_concurso
- **Definition:** One dated opening of a fund, with open/close dates and a status; a fund runs many calls over time.
- **Domain:** finance, supply
- **Why it matters:** Status/availability live at the call level, not the fund level — a fund can be "annual" while its current call is closed.
- **Also called:** concurso, convocatoria, llamado
- **Example:** "FPA 2026 was a single call of the standing FPA fund."



### co_benefit
- **Definition:** Additional positive effect of a mitigation action beyond direct emissions reduction.
- **Domain:** mitigation, planning, tef
- **Why it matters:** Co-benefits improve policy prioritization and action selection.
- **Also called:** co-benefits
- **Example:** "Switching to electric buses can improve air quality and reduce noise."

## E

### emissions_factor
- **Definition:** Conversion factor that translates one unit of activity data into emissions.
- **Domain:** emissions, methodology, inventory
- **Why it matters:** It is a core parameter in the formula `emissions = activity × emissions_factor`.
- **Also called:** ef
- **Example:** "kgCO2e per kWh for grid electricity."

## F

### funder_institution
- **Definition:** The body whose budget pays for a fund; not necessarily the body that operates the website or delivers the program (that is the provider/implementer).
- **Domain:** finance, actors
- **Why it matters:** Citation and licence follow the funder vs provider split (e.g. Min. Energía funds, AgenciaSE delivers). See `topics/data-sources/cl-climate-finance.md`.
- **Also called:** institución, organismo
- **Example:** "MMA is the funder_institution behind the FPR; municipalities apply."

## G

### gpc
- **Definition:** Global Protocol for Community-Scale Greenhouse Gas Inventories, a standard for city emissions accounting.
- **Domain:** emissions, inventory, standards
- **Why it matters:** It defines sector structure and reporting logic used in city inventories.
- **Also called:** global protocol
- **Example:** "Transport emissions are reported under GPC sector categories."

## I

### instrument_type
- **Definition:** The financing form of a funding opportunity: grant, loan, guarantee, blended, technical_assistance, or equity.
- **Domain:** finance, instruments
- **Why it matters:** Instrument shapes who can use it and how it scores (a loan to firms ≠ a grant to a municipality).
- **Also called:** instrumento
- **Example:** "CORFO Crédito Verde has instrument_type = loan."

## L

### locode
- **Definition:** UN/LOCODE city code used as the canonical city key in many datasets.
- **Domain:** city-identity, data-model, integration
- **Why it matters:** Correct use of `locode` prevents broken joins and city mismatches.
- **Also called:** actor_id
- **Example:** "`CL SCL` represents Santiago."

## M

### modal_shift
- **Definition:** Change in travel or freight demand from one transport mode to another.
- **Domain:** transport, mitigation, tef
- **Why it matters:** Mode changes can reduce energy demand and emissions at system level.
- **Also called:** shift in mode
- **Example:** "Shifting trips from private cars to electric rail."

## P

### proposal_postulacion
- **Definition:** A single submission to a funding call; awarded only if selected, and often filed by a technical presenter rather than the beneficiary.
- **Domain:** finance, awards
- **Why it matters:** Distinguishes a submission from an award and from the applicant/beneficiary; the presenter is a delivery-channel signal, not the beneficiary identity.
- **Also called:** postulación, proyecto postulado
- **Example:** "Most Bosque Nativo postulaciones are filed by an extensionista, not the owner."

## R

### revealed_fundability
- **Definition:** What awards data shows actually gets funded (where, how often, at what size), as opposed to what funding nominally exists.
- **Domain:** finance, awards, prioritization
- **Why it matters:** It corrects the availability bias of a supply-only inventory and feeds the fundability score; for a city it estimates mobilisation potential even when the city is not the applicant.
- **Also called:** awards signal, outcomes layer
- **Example:** "Many Bosque Nativo awards in La Araucanía signal a live route a city there can steer owners toward."

## T

### transition_element
- **Definition:** A TEF intervention unit representing a specific mitigation change, such as a shift or efficiency improvement.
- **Domain:** tef, mitigation, taxonomy
- **Why it matters:** It is the main building block used to organize and compare mitigation options.
- **Also called:** te, activity shift, outcome (in some HIAP docs)
- **Example:** "`shift_to_electric_vehicles` is one transition element."
