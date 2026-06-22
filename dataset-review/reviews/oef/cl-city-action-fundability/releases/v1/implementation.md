# Global-API database design — Chile city-action fundability

Status: **implemented**. Design for landing the Chile climate-finance work into `CityCatalyst/global-api`. Companion to `methodology.md` (the scoring logic). This doc covers the *production* shape: tables, the score, the API.

Author context: drafted 2026-06-19 from the v1 fixture and the global-api `modelled` conventions; reconciled to the as-built implementation 2026-06-22.

---

## As-built (authoritative)

The sections below (§1 onward) are the **original design proposal**, kept for rationale. Where they differ from this summary, **this summary is authoritative** — it reflects what was actually built.

**Modelled objects** (global-api Alembic revisions):

- `9f3c1a7b2e10` — `modelled.finance_opportunity` (+ `finance_opportunity_action` link table) — the supply catalogue.
- `a4f1c9d72b3e` — `modelled.finance_project` (+ `finance_project_action` link table) — precedent.
- `b8e2f5a1c9d4` — `modelled.city_finance_profile` — the CITY axes (autonomy / capacity / archetype).
- `c3f9a7e1d2b8` — `modelled.city_action_financial_feasibility(p_locode, p_country_code)` — the score, a set-returning **function** (no stored view).

**Pipelines** (cc-mage): `cl_finance_opportunity_to_modelled`, `cl_finance_project_to_modelled`, `cl_city_finance_profile_to_modelled` — bare S3 loaders → merge → catalog branch (per-source `release_id` from `index.yaml`) → release-scoped delete+insert.

**Endpoints** (all under the `climate-finance` namespace):

- `GET /api/v1/climate-finance/opportunities` — fund catalogue (filters: `sector`, `eligible_actor`, `status`).
- `GET /api/v1/cities/{locode}/climate-finance/feasibility` — the scored list (lean: score + `reason` + input counts + links).
- `GET /api/v1/cities/{locode}/climate-finance/actions/{action_id}` — drill-down: score + reachable funds (status, source url) + precedent projects.
- `GET /api/v1/cities/{locode}/climate-finance/projects` — precedent projects, across all actions (`?action_id`, `?scope=comuna|sector`).

**Key deviations from the proposal below:**

1. **No `finance_action` view (§3.3).** The score is derived **at read time** by the SR-function `city_action_financial_feasibility(...)` over the base tables — the methodology B7 route/score is inlined; release pinning is "latest of each." This replaces both the proposed view and the proposed app-layer computation.
2. **Action matches are a link table, not columns.** `finance_project` has no `action_id`/`match_label`; matches live in `modelled.finance_project_action` (`confidence ∈ {strong, goal_aligned}`), mirroring `finance_opportunity_action` — a project can carry several matches.
3. **`city_archetype` uses city-facing strength labels:** `Self-sufficient` / `Delivery-ready` / `Well-resourced` / `Support-ready`.
4. **Descriptive base columns are English**, with a companion `<col>_i18n` JSONB `{es, en}` (`project_name_i18n`, `sector_i18n`).
5. **Dropped (no consumer):** `beneficiaries_total` (finance_project) and `comuna_cut` (city_finance_profile).
6. **`actor_id` = city locode**, resolved from comuna via the `cl-ocha-ab` lookup; the 4 comunas without a locode are dropped from the city layer.
7. **Opportunities filters trimmed** to `sector` / `eligible_actor` / `status`; path is `/climate-finance/opportunities`.
8. **No separate `channels` endpoint** — the public-investment-by-precedent nuance is carried by the score's `route` + `reason` + `fund_access` and the action drill-down.

**Outstanding (live-DB confirmations):** the action→GPC-sector derivation from `action_pathway_mitigation_impact.gpc_reference_number`; the `action_pathway` `investment_cost` / `intervention_type` vocabularies (non-matching values band to the 0.5 midpoint).

---

## 1. Guiding decisions

Four decisions frame everything below; they were settled before the schema was drawn.

1. **Store the inputs, derive the score.** The precomputed `fundability_scored.csv` (≈35k rows = 345 comunas × 102 actions) was built to *test the methodology*, not to be the system of record. Persisting it would cache a cross-product that goes stale the moment any input changes, and it hides the logic behind a single scalar. Instead we store the score's *inputs* as tables and compute the score at read time in the API. The score is then auditable by construction — the response carries the inputs it was derived from — and never stale.

2. **Country-agnostic structure.** The conceptual model is universal; Chile specifics (FNDR, comuna, UTM, RATE) are *values*, not tables. Tables are named `finance_*` and carry a `country_code`, matching how `modelled.project_portfolio` already works. Adding another country adds rows, not tables.

3. **Lean to two base tables + a view, not six.** Only `finance_opportunity` and `finance_project` are new base tables for v1. `finance_action` is a **view** over the existing `modelled.action_pathway` table (which already carries `intervention_type`, `investment_cost`, `implementation_timeline`) joined to a benchmark roll-up from `finance_project` — so action demands have a single source of truth and nothing is duplicated. Two further conceptual-model tables are folded into the two base tables (funder denormalized onto opportunities; the project↔funding link folded into a JSONB column on the project). The CITY layer (`city_finance_profile`) lands in Phase 2. See §4 for the reasoning and the promotion triggers.

   **Reuse what exists.** `action_pathway` is the canonical action data; `finance_action` derives from it rather than restating it. `action_id` stays a plain string (no FK), matching `action_mitigation_feasibility_chain.src_action_id`.

4. **Follow global-api house conventions exactly.** `modelled` schema; UUID PKs via `gen_random_uuid()`; a natural key as a `UniqueConstraint`; every row FK'd to `modelled.dataset_release` via `release_id` (immutable, versioned releases with `is_latest`); `created_at`/`updated_at` defaulting to `NOW()`; `source_dataset` carried on every row; indexes on `release_id` and `(release_id, country_code, <key>)`. Migrations are Alembic revisions (template: `5f3e9f2b1c7d_create_modelled_project_catalog_table`); there are no SQLAlchemy model classes (the repo is migration-first).

---

## 2. The shape in one picture

```mermaid
erDiagram
    ACTION_PATHWAY       ||..o{ FINANCE_ACTION  : "view derives demands from"
    FINANCE_PROJECT      ||..o{ FINANCE_ACTION  : "view rolls up benchmarks from"
    FINANCE_ACTION       ||--o{ FINANCE_PROJECT : "instanced by (action_id, soft)"
    FINANCE_OPPORTUNITY  }o..o{ FINANCE_ACTION  : "matched by sector + actor (at read time)"
    CITY_FINANCE_PROFILE ||..o{ SCORE           : "autonomy/capacity (Phase 2)"
    FINANCE_ACTION       ||..o{ SCORE           : "demands"
    FINANCE_OPPORTUNITY  ||..o{ SCORE           : "reachable funds"
    FINANCE_PROJECT      ||..o{ SCORE           : "precedent (n_existing_projects)"

    FINANCE_ACTION { note "VIEW over action_pathway + finance_project roll-up" }
    SCORE          { note "DERIVED at read time in the API — not a table" }
```

Two base tables land now (`finance_opportunity`, `finance_project`) plus the `finance_action` **view**; one table lands when the SINIM city data is productionized (`city_finance_profile`). The `SCORE` is not stored — it is computed in the endpoint from these.

---

## 3. Tables to land now (Phase 1)

All in schema `modelled`, all release-versioned. Types follow the global-api conventions (UUID PK, Numeric for money/scores, JSONB for arrays/structured fields, timestamptz with `NOW()` default).

### 3.1 `finance_opportunity` — the supply catalogue

One row per fund/program-call a city could pursue or facilitate. Funder attributes are denormalized in (see §4.1). Source: the ten `cl-*/cl-*-fondos` reviews unioned via `oef/cl-finance-inventory`, plus MTT and the FPA fund.

| Column | Type | Notes |
|---|---|---|
| `opportunity_id` | UUID PK | `gen_random_uuid()` |
| `source_opportunity_id` | varchar, not null | natural key, e.g. `fpa-2026-proyectos-sustentables-ciudadanos` |
| `opportunity_name` | text, not null | |
| `funder_name` | varchar | denormalized funder display |
| `funder_level` | varchar | national / regional / local / multilateral |
| `funder_channel` | varchar | descriptor: competitive fund / public investment / intermediated multilateral (denormalized; no Route A/B/C) |
| `instrument` | varchar | grant / loan / guarantee / blended / technical_assistance / equity |
| `gpc_sectors` | JSONB | array, e.g. `["waste","stationary_energy"]` |
| `eligible_actor` | varchar | municipality / community / household / firm / NGO / … |
| `city_application` | varchar | **how the city transacts: `direct` / `facilitated` / `intermediated`** (replaces `city_can_apply` + the free-text `access_pathway`) |
| `funding_channel` | varchar | **what kind of channel it is: `competitive fund` / `public investment` / `intermediated`** (replaces `access_route`, drops the Route A/B/C prefix) |
| `access_tier` | varchar | **the access barrier within the channel: `competitive` / `BIP-SNI-gated` / `intermediated`** (methodology B5/B12). This is what flags the public-investment feeders (FNDR, FRIL, PMU, PMB, …) as reached through the SNI/BIP gate rather than an open concurso. Will gain finer values (`self-service`, `direct-application`) once curated |
| `open_date` | date | call opens — from source `open_date` |
| `close_date` | date | call closes — lets the API show closures over time across releases |
| `status` | varchar | open / closed / rolling |
| `status_as_of` | date | when `status` was last observed |
| `recurrence` | varchar | annual / ongoing / sporadic / one-off |
| `amount_clp` | Numeric | native amount where the source gives one (nullable; mostly absent) |
| `amount_note` | text | free text qualifier |
| `climate_relevance` | varchar | explicit / climate-adjacent / indirect |
| `specificity` | varchar | sector-specific / broad |
| `source_url` | text | provenance |
| `country_code` | varchar(2) | `CL` |
| `source_dataset` | varchar | review id |
| `release_id` | UUID FK | → `modelled.dataset_release` |
| `created_at` / `updated_at` | timestamptz | `NOW()` |

Unique: `(release_id, country_code, source_opportunity_id)`. Indexes: `release_id`; `(release_id, country_code, eligible_actor)`; `(release_id, country_code, close_date)`; GIN on `gpc_sectors`.

**On `city_application` vs `funding_channel` (your question — they are different, and both earn their place).** `city_application` is *the city's relationship to the money* — can it apply for itself (`direct`, e.g. FPA), must it help someone else who applies (`facilitated`, e.g. CONAF private owners), or is it reached only through a gatekeeper (`intermediated`, e.g. GCF). `funding_channel` is *what kind of instrument the fund is* — a competitive concurso, the public-investment (SNI/BIP) system, or intermediated multilateral money. They correlate but don't determine each other: a competitive fund can be either `direct` (FPA) or `facilitated` (CONAF). The score's access barrier reads `city_application`; `funding_channel` is context for display and matching. The old `city_can_apply` (`yes`/`facilitated`/`no-intermediated`) and `access_pathway` carried the same idea twice in different words — collapsed into `city_application`. The Route A/B/C labels are dropped everywhere in favour of the plain descriptors. If on reflection you find `funding_channel` redundant with `city_application` in practice, it's the one to drop.

### 3.2 `finance_project` — precedent (what got built, how it was paid)

One row per funded/awarded/formulated project. Co-finance sources are folded into a JSONB array (see §4.2). Source: BIP (Route B), CONAF and FPA awards (Route A), GCF Chile (Route C).

| Column | Type | Notes |
|---|---|---|
| `project_id` | UUID PK | |
| `source_project_id` | varchar, not null | natural key, e.g. `30044764-0` |
| `action_id` | varchar, nullable | soft link to `finance_action.action_id`; blank for unmatched (e.g. raw CONAF) |
| `project_name` | text, not null | |
| `sector` | varchar | mixed taxonomy — CONAF uses GPC `afolu`, BIP keeps its own source sector names (a known mapping gap) |
| `jurisdiction` | varchar | source label, e.g. `ARAUCO` |
| `actor_id` | varchar, nullable | resolved from `comuna_cut` at load where available (~48% of projects carry a comuna) |
| `lifecycle_stage` | varchar | formulated / appraised / financed / in-execution / completed |
| `evaluation_verdict` | varchar | RATE etc.; sparse |
| `cost_total` | Numeric | |
| `amount_committed` | Numeric | |
| `amount_paid` | Numeric | |
| `amount_unit` | varchar | `CLP_millions`, `UTM`, … (see §6) |
| `duration_months` | Numeric | |
| `beneficiaries_total` | integer | |
| `owner_formulator` | text | |
| `match_label` | varchar | strong / goal_aligned / … (quality of the action match) |
| `funding_channel` | varchar | descriptor only: `competitive fund` / `public investment` / `intermediated multilateral` (no Route A/B/C) |
| `funding_sources` | JSONB | array of `{source_label, funder_name, source_opportunity_id?, amount, amount_unit, paid_amount, cycle}` |
| `country_code` | varchar(2) | |
| `source_dataset` | varchar | |
| `release_id` | UUID FK | |
| `created_at` / `updated_at` | timestamptz | |

Unique: `(release_id, country_code, source_project_id)`. Indexes: `release_id`; `(release_id, country_code, action_id)`; `(release_id, country_code, actor_id)`; `(release_id, country_code, sector)`.

### 3.3 `finance_action` — a **view**, not a table

The ACTION layer is almost entirely derivable, so it lands as `modelled.finance_action` (a view), not a stored table. It reads from `modelled.action_pathway` (the canonical action data — already carries `intervention_type`, `investment_cost`, `implementation_timeline` per `src_action_id`) and joins a benchmark roll-up computed from `finance_project`. `action_id` is a plain string (no FK), matching `action_mitigation_feasibility_chain`.

Two pieces make up the view:

**(a) Demands — banded from `action_pathway` via `CASE`:**

| View column | Derived from | Banding |
|---|---|---|
| `action_id`, `action_name`, `sector` | `action_pathway` | passthrough |
| `intervention_type` | `action_pathway.intervention_type` | passthrough (this *is* the old `archetype`) |
| `capital_intensity` | `action_pathway.investment_cost` | low → 0.2 · medium → 0.5 · high → 0.8 |
| `preparation_complexity` | `action_pathway.intervention_type` | regulatory → 0.2 · planning/program/financial → 0.5 · infrastructure → 0.8 (infrastructure + high cost → 0.9) |

**(b) Benchmarks — aggregated from `finance_project` (only `match_label IN ('strong','goal_aligned')`), grouped by `action_id`:**

| View column | Aggregate |
|---|---|
| `bench_n_projects` | `count(*)` |
| `bench_duration_median_months` | `percentile_cont(0.5) … duration_months` |
| `bench_duration_n` | count of non-null durations |
| `bench_cost_median_mmclp` | `percentile_cont(0.5) … cost_total` |
| `bench_cost_n` | count of non-null costs |
| `match_confidence` | dominant `match_label` — **quote benchmarks only when `strong`** |

**Why a view wins.** The two demands are just bandings of `investment_cost` and `intervention_type` (the methodology's own mapping), and the benchmarks are a roll-up of `finance_project`. Storing them as a table would duplicate `action_pathway` and risk drift; a view keeps one source of truth and updates automatically when either input changes.

**The naming you flagged.** `archetype` → **`intervention_type`** (reuse the existing column name outright). `capital_demand` → **`capital_intensity`** (the methodology's own term — *how much money the action needs*; tested against the city's financial **autonomy**). `formulation_demand` → **`preparation_complexity`** — *how much technical work it takes to prepare/formulate the action into a fundable project* (a regulatory change is cheap to prepare → 0.2; an infrastructure build is demanding → 0.8); tested against the city's delivery **capacity**. So the two demands map cleanly onto the two city axes: money-need ↔ autonomy, preparation-need ↔ capacity.

**One thing to decide for the view (§ open items).** `action_pathway` and `finance_project` carry their *own* `release_id` lineages (different datasets). The view must pin a release for each side — default to each side's latest (`is_latest`/most-recent `retrieved_at`), or take an explicit pair. Stated as an open item below. Coverage of the demand columns is inherited from `action_pathway` (NULL where `intervention_type`/`investment_cost` are blank at source) — the same sparsity the fixture handled by backfilling.

---

## 4. The two simplifications, and how to reverse them

These are deliberate v1 reductions, each with a stated trigger for promotion to a full relational table.

### 4.1 Funder folded into opportunity

There are ~18 funders and `opportunities.csv` already carries `funder_name`. For v1 the funder-level fields the API needs (`funder_name`, `funder_level`, `funder_route`) are denormalized onto `finance_opportunity` and onto each `funding_sources` entry on a project. **Cost:** updating a funder attribute touches many rows — but rows are immutable within a release, so this is a non-issue. **Promote to a `finance_funder` dimension when:** funders need to be listed/queried independently of their opportunities (e.g. a "who funds in this country" view), or funder attributes grow beyond a handful of display fields.

### 4.2 Project↔funding link folded into JSONB

The conceptual model has a `project_funding` link (the many-to-many where co-finance lives). For v1 it is a JSONB `funding_sources` array on `finance_project`. **Why it's safe now:** per-source amounts are mostly blank for BIP (the source records project totals and a *list* of sources, not the split); there is no award-grain data with independent amounts; and the city-facing reference views only need to *show* a project's sources, not query across them. **Cost:** loses relational queries like "every project FNDR funded" or "sum of CONAF bonificación by cycle." **Promote to a relational `finance_project_funding` table when:** cross-funder analytics are needed, or award/disbursement-grain data with real per-source amounts arrives.

### 4.3 The precomputed score, dropped entirely

Not landed in any form. The score is computed in the API from §3 (+ §5.1). If a precomputed/materialized score is ever needed (e.g. bulk export, analytics at national scale), add it as an explicit **cache** of a visible computation — never as the source of truth.

---

## 5. The CITY layer and the score (Phase 2)

### 5.1 `city_finance_profile` — the CITY axes

The score's CITY layer (financial autonomy, delivery capacity) is **not** in the finance data — it comes from the SINIM + censo reviews and today exists only inside the precomputed `fundability_scored.csv`. Productionizing the score therefore depends on a separate dataset landing. When it does, it lands as one small table:

| Column | Type | Notes |
|---|---|---|
| `city_profile_id` | UUID PK | |
| `actor_id` | varchar, not null | the API key |
| `comuna_cut` | varchar | CUT code, provenance |
| `autonomy` | Numeric | 0–1, `1 − fcm_dependency_pct/100` |
| `capacity` | Numeric | 0–1, staff-percentile blend |
| `city_archetype` | varchar | self-starter / capable-but-cash-tight / funded-but-thin / needs-full-support |
| `country_code` | varchar(2) | |
| `source_dataset` | varchar | SINIM review |
| `release_id` | UUID FK | |
| `created_at` / `updated_at` | timestamptz | |

Unique: `(release_id, actor_id)`. ~345 rows for Chile — replaces the 35k-row precomputed cross-product with a per-city input table.

### 5.2 How the score is derived

At read time the endpoint runs the methodology's interaction (`methodology.md` B4–B7) over the inputs:

- **ACTION** demands (`capital_intensity`, `preparation_complexity`) from the `finance_action` view.
- **CITY** axes (`autonomy`, `capacity`) from `city_finance_profile` — or the methodology's **neutral fallback (0.50)** when the city has no profile.
- **FINANCE** resolution: match `finance_opportunity` to the action by GPC sector × eligible actor × usability (`status`/`recurrence`) × access pathway → a route bucket and `fund_access`.
- **PROJECTS** evidence: `n_existing_projects` = count of `finance_project` rows for the action (and/or comuna).

The bucket→`financial_feasibility` map (B7) is tunable config in app code, not SQL — so the methodology owner can adjust bands without a migration. The neutral fallback means **the score endpoint works the day Phase 1 lands**, returning a finance-side, city-neutral feasibility; Phase 2 sharpens it per city.

> Note on the function-vs-table question: the mitigation endpoint reads from a Postgres set-returning function because it *computes* its score in SQL across indicator tables. Our score is derived from far fewer inputs and the logic is still exploratory, so v1 computes in the **app layer** (transparent, easy to tune). A thin `modelled.city_action_financial_feasibility(...)` function wrapper can be added later for signature parity if desired — over the same input tables, still not a stored score.

---

## 6. Amounts, units, and provenance (read honestly)

- Amounts are stored **raw with their unit** (`amount_unit`): BIP in `CLP_millions`, CONAF in `UTM`. No normalized currency column for v1 — adequacy (amount vs cost) is explicitly *not measured* by the methodology and amounts are mostly absent. Add a normalized column only when amounts firm up enough to be worth it.
- `project.sector` mixes taxonomies (CONAF GPC `afolu` vs BIP's own sector names). Mapping BIP→GPC is a known next step; until then, sector filters must account for both vocabularies.
- `evaluation_verdict`, `duration_months`, `actor_id` and amounts are **sparse by source**, not by error. Roughly 48% of projects carry a comuna.
- Every row carries `source_dataset`; the upstream review remains authoritative for licence and per-source caveats. Licence inheritance is the most-restrictive-upstream rule (binding constraint today: SINIM, non-commercial + attribution) — see `methodology.md` B11 before any redistribution.

---

## 7. API design

A small family under a `climate-finance` namespace, keyed by `actor_id`. Three of your goals are three different views — the score, the opportunities reference, the projects reference — so they are separate, independently cacheable resources, plus one composed drill-down.

```
GET /api/v1/cities/{actor_id}/climate-finance/feasibility            # scores, with full input breakdown
GET /api/v1/cities/{actor_id}/climate-finance/opportunities          # reachable funds (reference)
GET /api/v1/cities/{actor_id}/climate-finance/projects               # precedent projects (reference)
GET /api/v1/cities/{actor_id}/climate-finance/actions/{action_id}    # one action: score + funds + precedent, composed
```

All responses follow the house `meta` + `data` shape (cf. the CCRA Adapta endpoint), where `meta` carries release provenance and methodology status/caveats so the "working/exploratory" nature is never lost.

### 7.1 `feasibility` — transparency by construction

Every number that produced the score is surfaced under `inputs`, grouped by the four model layers, with a plain-language `reason`:

```jsonc
{
  "meta": {
    "actor_id": "...", "country_code": "CL",
    "release": { "version_label": "v1", "released_at": "2026-06-19", "source_dataset": "oef/cl-city-action-fundability" },
    "methodology": { "status": "working", "city_layer": "neutral-fallback",   // or "profiled" once Phase 2 lands
      "caveats": ["not a probability of funding", "coverage reflects what is catalogued"] }
  },
  "data": [{
    "action_id": "c40_0010",
    "action_name": "Introduce energy-efficiency standards for new residential buildings",
    "sector": "stationary_energy",
    "financial_feasibility": 1.0,
    "route": "self-deliverable",
    "reason": "Low-capital regulatory action; self-deliverable regardless of city finances.",
    "inputs": {
      "action":   { "intervention_type": "regulatory", "capital_intensity": 0.2, "preparation_complexity": 0.2 },
      "city":     { "autonomy": 0.84, "capacity": 0.74, "archetype": "self-starter" },  // null block under neutral fallback
      "finance":  { "fund_access": "competitive", "n_reachable_opportunities": 3 },
      "evidence": { "n_existing_projects": 5 }
    },
    "links": {
      "opportunities": ".../climate-finance/opportunities?action_id=c40_0010",
      "projects":      ".../climate-finance/projects?action_id=c40_0010"
    }
  }]
}
```

`reason` is composed at read time from the same inputs (consistent with the score being derived, not stored).

### 7.2 `opportunities` — reachable supply

Reads `finance_opportunity` filtered to the country and to municipality-reachable funds (`city_application`, `eligible_actor`), with `?action_id` or `?sector` to scope. **Honest framing:** opportunities are *national/regional supply*, not city-specific records — a city's "reachable opportunities" is the sector/actor-filtered view of national supply, not a per-city fund table.

### 7.3 `projects` — precedent

Reads `finance_project` with `?scope=comuna|sector` — "precedent in *your* comuna" vs "sector precedent nationally" — plus `?action_id`. Each project exposes its `funding_sources` so the city sees how comparable work was paid for.

### 7.4 `actions/{action_id}` — the drill-down

Composes the three: the action's score block (the `inputs` breakdown), its reachable opportunities, and its precedent projects — the "explain this score and show me the evidence" view.

### 7.5 `channels` — making public investment an evidenced route, not a gap

Public investment (the SNI/BIP system) has **no application form** — a city doesn't apply to a fund, it formulates an *iniciativa*, passes the SNI/BIP gate, then draws a feeder fund (FNDR, Sectorial, Municipal). If the API only listed competitive opportunities, this channel — the one that actually funds the most municipal work (787 BIP projects, FNDR-dominant, reaching 41 actions) — would vanish and the action would read as a gap. It is also the most-used channel for exactly the actions (transport, infrastructure) where competitive municipal supply is thinnest.

The fix is a per-action `channels` block (on `feasibility` rows and the `actions/{id}` drill-down) that resolves all three channels, where **public-investment availability is driven by project precedent, not by a fund being "applyable"**:

```jsonc
"channels": {
  "competitive": {                              // from finance_opportunity (supply)
    "available": true, "n_sector_specific": 0, "n_broad": 40,
    "access_tier": "competitive (city or enabled actor applies to a concurso)" },
  "public_investment": {                         // availability from finance_project EVIDENCE
    "available": true,
    "access_tier": "BIP-SNI-gated — no application form; city formulates an iniciativa, passes the SNI/BIP gate, then draws a feeder fund",
    "feeder_funds": ["FNDR", "FRIL", "PMU", "PMB", "PMR", "FRC", "FRPD"],
    "evidence": { "n_precedent_projects": 11, "funded_via": {"FNDR": 11, "Sectorial": 1},
                  "example_comunas": ["Antofagasta", "Ñuñoa"] } },
  "intermediated": {                             // MTT operator subsidy / GCF accredited entity
    "available": true, "n_supply": 1, "n_precedent_projects": 0,
    "access_tier": "intermediated — via operator (transport subsidy) or accredited entity (multilateral)" },
  "is_real_gap": false                           // true only when NO channel is open
}
```

Two consequences worth stating:

- **A gap is reported only when it's real.** `is_real_gap` is true only when there is no competitive opportunity **and** no BIP precedent **and** no intermediated route. The transport example shows the honest nuance the old view lost: `competitive.n_sector_specific = 0` (no dedicated municipal concurso for transport), yet `public_investment.available = true` because 11 BIP projects prove the route — so it is *not* a gap.
- **The score should follow.** B7's "needs co-finance — no usable fund (gap) → 0.25" must not fire for an action with strong BIP precedent; the public-investment route is demonstrably open (it just runs through the gate). The route/`reason` annotation should name public investment as the channel when that is what the evidence shows. This aligns with the methodology's own coverage matrix (B9a), which already tracks "BIP precedent" as a first-class column.

**What this required on the data side.** The v1 fixture flattened every opportunity to `access_route = "Route A — competitive fund"`, so the feeder funds (FNDR, FRIL, PMU, PMB, …) came through mistagged as competitive and, being non-directly-applyable, dropped out of "reachable" entirely. The loader must instead read the real channel/tier from the source reviews (`cl-gore-fndr`, `cl-subdere-fondos`) and set `funding_channel = public investment`, `access_tier = BIP-SNI-gated`, `city_application = direct` (the city *is* the formulator — the gate is captured by `access_tier`, not by denying access). The re-tagging is implemented in finance_opportunity (funding_channel / access_tier / city_application); the public-investment-by-precedent nuance is carried by the score route/reason rather than a separate channels block (see the As-built summary above).

---

## 8. Rollout

**Phase 1 (now) — reference + city-neutral score.** One Alembic revision creating the two base tables (`finance_opportunity`, `finance_project`; template: `5f3e9f2b1c7d`) and the `finance_action` view. A loader (analogous to `build_finance_db.py`) reads the review CSVs and writes the base tables against a `dataset_release` row, resolving `actor_id` from `comuna_cut` at load. Endpoints: `opportunities`, `projects`, and `feasibility` running on the neutral CITY fallback. This delivers both reference views and a working (finance-side) score immediately.

**Phase 2 (when SINIM productionizes) — full score.** A second revision adds `city_finance_profile`; its loader fills autonomy/capacity per `actor_id`. The `feasibility` endpoint switches from neutral fallback to profiled per city automatically (the response's `meta.city_layer` flips `neutral-fallback` → `profiled`). Optionally add the SR-function wrapper for parity with the mitigation endpoint.

**Later, if needed.** Promote the funder dimension (§4.1) and/or the project-funding link (§4.2) per their triggers; add a normalized currency column (§6); map BIP sectors to GPC.

### Open items for sign-off

1. **CUT→actor_id mapping** — you have the lookup; confirm whether it lives in global-api already (for the loader to join against) or needs to come along.
2. **SINIM productionization timing** — gates Phase 2; Phase 1 does not depend on it.
3. **HIAP weight** — folding `financial_feasibility` into the Feasibility pillar (proposed legal 0.34 / mitigation 0.33 / financial 0.33) needs methodology-owner sign-off (Ayinawu) per `methodology.md` B7.
4. **`finance_action` view release-pinning** — the view crosses two release lineages (`action_pathway` and `finance_project`); confirm "latest of each" is acceptable vs an explicit release pair (§3.3).
5. **`funding_channel`** — keep it alongside `city_application`, or drop as redundant once you see it in use (§3.1).
