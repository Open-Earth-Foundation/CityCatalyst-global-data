# Methodology (working) — Chile climate-finance inventory & action financing-availability indicator

Status: **working / exploratory** (OEF). Not yet a Mage pipeline. This document is the hub methodology for the harmonized inventory and the action **financing-availability (coverage)** indicator built on it. It will move to `knowledge-base/topics/` only once it stabilises.

## 0. What this indicator is — and is NOT (read first)

This indicator measures **financing availability / coverage**: *does a climate-relevant public funding channel of the right sector exist, is it currently usable, and can a city access it?* It deliberately does **not** claim **fundability** in the sense of "this action tends to secure financing in practice." That distinction matters because a coverage indicator built from listed opportunities largely reflects *what we have catalogued* (availability bias), not real-world funding behaviour — sectors we have reviewed light up; unreviewed ones (e.g. transport) look like gaps regardless of reality.

"Fundable" bundles at least five separable things; this indicator covers only the first one and part of the second:

1. **Supply** — does a relevant, open funding channel exist? *(measured)*
2. **Access/eligibility** — can this actor apply and qualify? *(partially — actor-fit heuristic)*
3. **Adequacy** — does amount + instrument fit the action's cost/type? *(not measured — amounts mostly absent)*
4. **Competitiveness** — realistic odds of an award given demand/supply? *(not measured)*
5. **Capacity** — can the city prepare a winning application (e.g. SNI "RS")? *(not measured)*

True "what tends to be fundable in practice" would need **revealed outcomes** — award/disbursement history (the FPA/FPR "Fondos Adjudicados" archives, SUBDERE's awarded-project records). That is a deliberate **future** direction, not built here. Use this indicator as a *"where could a city look"* map and a *gap map*, with the availability-bias caveat stated, and never as a probability of getting funded.

## 1. The harmonized inventory

`chile_finance_inventory.csv` unions six vetted source reviews — `cl-mma` (environment/waste, 55), `cl-minenergia` (municipal energy, 6), `cl-subdere` (municipal infrastructure, 4), `cl-minvu` (urban/green, 4), `cl-gore` (regional FNDR, 4), `cl-corfo` (firm-facing debt/blended, 5) — into one row-per-fund table (78 rows) on a common schema. Source reviews remain authoritative for provenance, license, and per-source caveats; this inventory is a derived product, rebuilt by `harmonize.ipynb` after any source release.

Key harmonized fields the scoring relies on: `gpc_sectors`, `eligible_actor`, `specificity` (sector-specific | broad), `status`, `recurrence` (annual | ongoing | sporadic | one-off), `climate_relevance_norm` (explicit | adjacent | indirect), `detail_level` (detailed | index).

## 2. Financing-availability (coverage) indicator — design

Purpose: classify each action by **what kind of public funding channel covers it** — a dedicated (sector-specific) channel, only broad/general-purpose channels, or none. Output: a `coverage_level` label per action, not a fundability score or rank. The core constraint, carried from the failed SSG attempt: a broad inventory must not inflate coverage (broad funds can never count as a dedicated match).

It is two steps: **match** an action to inventory funds, then **classify** the action by its best match.

Coverage levels (from the match quality in §2b):
- **sector-specific** — ≥1 dedicated, currently-usable, city-accessible channel exists (best case).
- **broad-only** — no dedicated channel, but a general-purpose fund (PMU/FNDR-type) or a sector-specific fund with a gap covers it.
- **none** — no usable, accessible channel found (a true gap).

### 2a. Usability (a property of each fund, from this inventory)

Combine `status` with `recurrence` so a between-cycles fund isn't treated as dead:

- **usable_now** — `status` open/rolling, OR `recurrence = annual` (reliably reopens ~Aug–Oct), OR `recurrence = ongoing`.
- **not_currently_usable** — `recurrence` one-off/sporadic and `status` closed.

### 2b. Per-match fit (Strong / Moderate / Weak)

For an action matched to a fund (matched on sector relevance first):

- **Strong** = `specificity = sector-specific` AND fund is usable_now AND the action's implementer is a realistic `eligible_actor`.
- **Moderate** = sector-specific with one gap (e.g. not currently usable, or actor is facilitated/intermediated), OR a `broad` fund that is usable_now and accessible.
- **Weak** = `broad`/cross-sector only, or major actor/timing gap, or `detail_level = index` with unconfirmed specifics.

Control: a **`specificity = broad` fund can never be Strong** — capped at Moderate. This is the explicit fix for PMU/PMB/FRC and global funds matching everything.

### 2c. Action coverage_level (simple rules)

- **sector-specific** = ≥1 Strong match.
- **broad-only** = no Strong, but ≥1 Moderate.
- **none** = only Weak matches, or no match at all (a true gap).

(Counts of Strong/Moderate matches are retained per action as supporting columns, but they are **descriptive of supply breadth, not a ranking of fundability** — see §0. We deliberately do not emit an ordinal "most fundable" rank.)

## 3. What this does and does not claim

- It is a **coverage label**, not a fundability score or an ordinal rank (see §0).
- Quality depends entirely on (a) action↔fund **matching** and (b) the action's sector/actor metadata — neither is in this inventory; both come from the action set being scored.
- **Amounts are mostly absent** (only cl-mma detailed rows carry `amount_clp`; energy/SUBDERE/MINVU state rates or per-call figures) — do not rank on money.
- **`detail_level = index` rows are leads** — confirm the live call before treating as a Strong match.
- Broad funds are capped by design; do not "fix" this by promoting them.

## 4. Next steps before productionising

1. Bring in the **action set** (the mitigation/adaptation actions to score) with sector + implementer fields.
2. Define the **sector match** (GPC sector ↔ fund `gpc_sectors`) and the actor-eligibility match.
3. Classify coverage on real actions; sanity-check the Strong/Moderate cutoffs on observed output (the coverage notebook is the place).
4. Once stable, port `harmonize.ipynb` + the coverage classification to a Mage pipeline (blocks map nearly 1:1) and promote this methodology to `knowledge-base/topics/`.

## 5. Run — 2026-06-08 (`chile_financing_coverage.ipynb`)

Classified the ClimateView `current_actions` set (102 mitigation actions) against the 73-fund inventory. GPC subsector → fund-sector map: I→stationary_energy, II→transportation, III→waste (III.4 also water), IV→industry, V→afolu. Output: `financing_coverage_by_action.csv` (`coverage_level` per action).

What the run shows (mechanics are sound):
- Coverage splits **sector-specific 66 / broad-only 36 / none 0**; the eight broad funds (PMU, PMB, FRC, Quiero Mi Barrio, Pavimentación, FNDR, FRIL, FRPD) are capped at Moderate by construction — the SSG inflation does not recur.
- The **gaps surface honestly**: transportation and industry actions are `broad-only` because no dedicated fund exists for them (Min. Transporte and IPPU/industry are unreviewed). That's the catalogue gap, exactly the availability bias of §0 — not a "low fundability" finding about those actions.

Known limitation (consistent with §0): **coverage is essentially a property of the action's GPC sector, not the individual action** — every action in a sector gets the same label. Cause: funds are sector-tagged and every action is matched with one uniform implementer ("city"). This is acceptable for a *coverage/gap map* but is the reason this must not be read as action-level fundability. Finer resolution (were we to want it) would need signals the action set carries — implied eligible actor (residential vs municipal vs commercial), finer sub-sector (`gpc_reference_number`), instrument/cost fit (`investment_cost`) — but per the §0 decision we are NOT presenting this as fundability, so within-sector resolution is out of scope for now.

### 5a. Regional tier added — 2026-06-08 (`cl-gore`, inventory now 73)

Added the GORE/FNDR regional instruments (FNDR investment, FRIL, 8% Medio Ambiente line, FRPD). Re-ran: **coverage levels unchanged** — three of the four are `specificity=broad` (capped) and the one sector-specific line (8% Medio Ambiente) has an NGO actor. Mean matches/action rose 47→51 (more breadth) but the dedicated-coverage picture held. This **confirms the gap point**: more broad funds widen coverage but do not turn a `broad-only` sector into `sector-specific` — that needs a dedicated fund (e.g. Min. Transporte). Adding GORE improves the inventory and the city-facing reference, not the coverage ceilings.

Bug caught & fixed in the same run: the actor-fit check matched the substring "municipal" inside "NOT municipalities" (FNDR 8% line), wrongly granting a dedicated match; added a negation guard. A reminder that the string-based actor match is a heuristic.

### 5b. CORFO (firm-facing debt/blended) added — 2026-06-08 (`cl-corfo`, inventory now 78)

Added CORFO's instruments (Crédito Verde, Expande, guarantees, green-hydrogen facility, Innova) — the debt/blended tier and the private-firm actor that the SSG-vs-inventory gap analysis flagged as the biggest single hole. Re-ran: **city coverage unchanged**, and crucially **`industry` stayed `broad-only`** even though CORFO adds *sector-specific* industry/energy instruments. The reason is decisive for interpretation: CORFO's `eligible_actor` is the **firm**, not the city, so under the city-actor lens these are not dedicated city channels. This is the clearest evidence yet that the industry (and much of the energy/transport) coverage gap is an **actor gap, not a supply gap** — cities don't implement industrial decarbonisation, firms do, financed by CORFO via loans/guarantees. It also adds the instrument diversity (loans/guarantees/blended) the grant-only inventory lacked. Takeaway for any future move beyond a coverage map: coverage must be read against *who implements the action*, which is why action-actor inference (§5) is the real next step — not more sources.
