# Methodology (working) — Chile city-action fundability

Status: **working / exploratory** (OEF). Not yet a Mage pipeline; moves to `knowledge-base/topics/` only once it stabilises. This is the hub for the consolidated product (it replaces the former `cl-finance-inventory` and `cl-action-fundability` methodologies). It has two parts: **Part A — supply & coverage** (the finance inventory and a financing-availability indicator) and **Part B — the fundability model** (the four-layer model that consumes Part A).

---

# Part A — Supply & coverage (the FINANCE layer)

## A0. What this measures — and what it does NOT (read first)

Part A measures **financing availability / coverage**: *does a climate-relevant public funding channel of the right sector exist, is it currently usable, and can a city access it?* It deliberately does **not** claim **fundability** in the sense of "this action tends to secure financing in practice." A coverage indicator built from listed opportunities largely reflects *what we have catalogued* (availability bias), not real-world funding behaviour — reviewed sectors light up, unreviewed ones look like gaps regardless of reality.

"Fundable" bundles five separable things; Part A covers the first and part of the second: **supply** (does a channel exist — measured), **access/eligibility** (can this actor apply — partial, actor-fit heuristic), **adequacy** (amount vs cost — not measured, amounts mostly absent), **competitiveness** (award odds — not measured), **capacity** (can the city prepare a winning application — not measured). True revealed fundability needs award/disbursement history; that is a future direction. Use Part A as a *where-to-look* + *gap* map, never as a probability of getting funded.

## A1. The harmonized inventory

`data/chile_finance_inventory.csv` unions **ten** vetted source reviews into one row-per-fund table (**99 rows**): cl-mma 55, cl-indap 9, cl-mop 7, cl-minenergia 6, cl-corfo 5, cl-subdere 4, cl-minvu 4, cl-gore 4, cl-mtt 3, cl-conaf 2. Source reviews remain authoritative for provenance, licence and per-source caveats; this inventory is a derived product, rebuilt by `01_finance_inventory.ipynb` after any source release. Key harmonized fields the scoring relies on: `gpc_sectors`, `eligible_actor`, `specificity` (sector-specific | broad), `status`, `recurrence` (annual | ongoing | sporadic | one-off), `climate_relevance_norm`, `detail_level`.

## A2. The coverage indicator — design

Classify each action by **what kind of public funding channel covers it** — a dedicated (sector-specific) channel, only broad/general-purpose channels, or none. Output: a `coverage_level` label per action, not a score or rank. The core constraint (carried from the failed SSG attempt): a broad inventory must not inflate coverage — broad funds can never count as a dedicated match.

Two steps: **match** an action to inventory funds (sector relevance first), then **classify** by best match.

- **Usability** combines `status` with `recurrence` so a between-cycles fund isn't treated as dead: `usable_now` if open/rolling, or `recurrence = annual` (reliably reopens ~Aug–Oct), or `ongoing`; else `not_currently_usable`.
- **Per-match fit:** **Strong** = sector-specific AND usable_now AND realistic `eligible_actor`. **Moderate** = sector-specific with one gap, OR a usable, accessible broad fund. **Weak** = broad/cross-sector only, or major actor/timing gap. Control: a **broad fund can never be Strong** (capped at Moderate) — the explicit fix for PMU/PMB/FRC and global funds matching everything.
- **Action `coverage_level`:** `sector-specific` = ≥1 Strong; `broad-only` = no Strong but ≥1 Moderate; `none` = only Weak or no match.

## A3. Run — coverage result

Classified the ClimateView `current_actions` set (102 mitigation actions) against the inventory. Coverage splits **sector-specific 66 / broad-only 36 / none 0**; the broad funds (PMU, PMB, FRC, Quiero Mi Barrio, Pavimentación, FNDR, FRIL, FRPD) are capped at Moderate by construction — the SSG inflation does not recur. Gaps surface honestly: transportation and industry actions are `broad-only` because no dedicated *city* channel exists (the funds that do exist are operator- or firm-facing).

**Known limitation:** coverage is essentially a property of the action's GPC **sector**, not the individual action — every action in a sector gets the same label, because funds are sector-tagged and each action is matched with one uniform implementer ("city"). Acceptable for a coverage/gap map; the reason it must not be read as action-level fundability. The decisive finding from adding CORFO and the operator-facing transport/agriculture funds: the industry/transport "gap" is largely an **actor gap, not a supply gap** — cities don't implement industrial decarbonisation or run bus fleets, firms and operators do. Coverage must be read against *who implements the action*, which is why action-actor inference is the real next step, not more sources.

---

# Part B — The fundability model (ACTION × CITY → FINANCE)

## B0. What this models — and what it does not

For a **specific comuna** and a **specific climate action**: *how hard will it be to fund and deliver, and by what route?* Output: a **categorisation** (route/effort bucket + a 0–1 `financial_feasibility` score + the funds that fit), feeding the MEED+ HIAP **Feasibility** pillar. It is **not** a probability of securing finance, **not** a ranking of comunas, and it **never** lowers an action's impact because a city is weak (a hard action in a weak comuna is *harder / needs an external route*, not *less worth doing*). Objective scope: order *actions within a single comuna* by difficulty — distinguishing difficulty *between* comunas is explicitly not required.

## B1. The four layers

| Layer | Source | Role | Partition we claim | Join key |
| --- | --- | --- | --- | --- |
| **ACTION** (what) | actions catalog (102), `cl-ssg-projects` | the thing being funded | **capital intensity** (`investment_cost`) + **formulation demand** (from `primary_intervention` archetype) | `action_id`, GPC sector |
| **CITY** (who) | `cl-subdere-sinim` + `cl-ine-censo` | can the comuna pay & deliver | continuous **autonomy** & **capacity** scores (2×2 as summary) | CUT (`comuna_cut`) |
| **FINANCE** (route) | the harmonized inventory (Part A; 99 funds, municipality-eligible subset) | which money the city can reach | usable, city-eligible funds by sector + **access barrier** | GPC sector × eligible-actor |
| **PROJECTS** (evidence) | ficha / `project_action_matches`; CONAF/FPA/GCF awards | reality check & precedent | descriptive only | CUT + project↔action matches |

**Forward model = ACTION × CITY → FINANCE.** PROJECTS is the **evidence** layer (calibrates, illustrates, lends precedent) — not a forward input (size-confounded; only ~48% of projects carry a comuna; predicting with it would be circular).

## B2. The CITY layer

Two axes, kept separate (2025 correlation r ≈ 0.22 — they measure different things):

- **Financial autonomy** (0–1, higher = more own-money) — `1 − fcm_dependency_pct/100`, supported by `ipp_percapita_mclp`, `presup_percapita_mclp`.
- **Delivery capacity** (0–1) — `0.7 × percentile(staff_profesional_total) + 0.3 × percentile(professionalization_pct)`. Continuous, not a fixed cut.

Four **archetypes** summarise the two scores: self-starter (High/High), capable-but-cash-tight (Low-fin/High-cap), funded-but-thin (High-fin/Low-cap), needs-full-support (Low/Low). They split **20 / 44 / 67 / 214** on 2025 data (~62% needs-full-support). **Guardrails (SINIM review):** coarse tiers, never a fine rank; never read fiscal strength from per-capita income alone (rural/mining micro-comunas look rich per-cápita but are weakest); staff counts exclude *honorarios*, so they understate small comunas and nulls ≠ zero.

## B3. The ACTION layer

- **Capital intensity** — `investment_cost` (low/med/high → 0.2/0.5/0.8). Loads onto financial autonomy.
- **Formulation demand** — from the catalog's `primary_intervention` archetype (backfilled from `primary_channel` for the 33 blanks), covering all 102 with no Chile-specific legal data: regulatory 0.2 · planning/program/financial 0.5 · infrastructure 0.8 (infrastructure + high cost → 0.9). Loads onto delivery capacity.
- **Self-financeability** — dropped as a separate tag; it emerges (a low-capital action is self-deliverable by construction, and otherwise FINANCE says whether a direct-access route exists).

Choosing the catalog archetype over MEED legal scores keeps the model **portable to any CityCatalyst city** (the catalog is the global C40/IPCC/ICare set); MEED is Chile-only, used here for validation, not derivation.

## B4. Interaction → route buckets

Each action demand is tested against the axis it loads on; a shortfall sets the route. Low-capital actions are flat across comunas (money isn't the constraint); demanding actions diverge.

| | Low-capital | High-capital |
| --- | --- | --- |
| **High autonomy** | self-deliverable | own-budget feasible |
| **Low autonomy** | self-deliverable | needs external co-finance |

…and high **formulation demand** vs **low capacity** escalates with *"+ technical assistance / pooling"*. **The five buckets (easy → hard):** self-deliverable · own-budget feasible · needs technical assistance · needs external co-finance · needs external finance + TA / pooling. No single capacity/autonomy cut exists — both axes are continuous and the threshold that matters is action-specific. Demand bands are tunable config; within-city ranking was shown invariant to ±0.1 band jitter (median Spearman ≈ 1.0).

## B5. FINANCE resolution

Resolve the route bucket against the inventory by **sector** (action GPC ↔ fund `gpc_sectors`), **eligible actor** (the municipality-eligible subset — a minority of the 99 funds; many are firm-, operator- or household-facing), **usability** (`status`/`recurrence`), and **access pathway**.

**Access pathway feeds back onto capacity:** a direct-application grant (e.g. FPA) is reachable even by a weak comuna; a BIP/SNI-gated fund (FNDR) is not — so the same fund is "accessible" for a self-starter and "needs TA to access" for a weak comuna.

**Caveat — the `fund_access` flag is a weak heuristic.** It is currently a substring match ("direct" in the `access_pathway` text). It is string-fragile, conflates the direct-application *channel* with *non-competitive* (those funds are still competitive grants), and does not detect the **BIP/SNI gate**, which is the real capacity barrier. The fix is to curate an explicit `access_tier` (self-service / direct-application / competitive / BIP-SNI-gated); until then the direct-vs-competitive split is low-confidence.

## B6. PROJECTS evidence layer

Descriptive only: **calibrate** the capacity read (which comunas actually formulate BIP projects); **existing projects per action** (`project_action_matches`); **funded precedent** (CONAF, FPA and GCF award crosswalks now populate precedent, so it is multi-sector — see B9a). Not a forward input (B1).

## B7. The `financial_feasibility` score & HIAP integration

The route bucket (blended with fund access) maps to a 0–1 score plugged into HIAP's **Feasibility** pillar as a third leg (legal · mitigation · financial):

| Bucket | `financial_feasibility` |
| --- | --- |
| self-deliverable | 1.00 |
| own-budget feasible | 0.85 |
| needs technical assistance | 0.70 |
| needs co-finance — direct fund | 0.60 |
| needs co-finance — competitive fund | 0.45 |
| needs co-finance — no usable fund (gap) | 0.25 |
| needs finance + TA / pooling | 0.15–0.35 (by fund access) |
| no data (non-pilot city) | **0.50 neutral** |

**Integration:** proposed **legal 0.34 / mitigation 0.33 / financial 0.33**. Feasibility is ~0.23 of the HIAP final score, so financial feasibility is ~0.07 of the total — enough to break ties and nudge, not enough to swamp Impact (0.55). Weight changes require methodology-owner (Ayinawu) sign-off. The highest-value use is the **annotation**, not the score: attach the bucket, named funds (+ access type) and precedent to each ranked action.

## B8. Output specification

Per `(action × comuna)`: `comuna_cut`, `comuna`, `autonomy`, `capacity`, `action_id`, `action_name`, `archetype`, `sector`, `capital_demand`, `formulation_demand`, `route`, `fund_access`, `financial_feasibility`, `n_existing_projects`. Delivered as `data/fundability_scored.csv` (345 × 102 = 35,190 rows). Feeds HIAP Feasibility with the reason attached — never Impact or Alignment.

## B9. Results — national run (345 comunas × 102 actions)

- **Route mix:** self-deliverable 14.4% · own-budget 7.7% · needs TA 17.0% · needs co-finance 19.2% · needs finance + TA / pooling 41.7%. So ~22% of all (action, comuna) pairs are doable unaided and ~78% need external support — the expected consequence of most comunas being low-autonomy.
- **By archetype, `financial_feasibility` orders intuitively:** infrastructure 0.44 < program 0.54 < planning 0.55 < financial 0.60 < regulatory 0.81.
- **Validity checks:** `financial_feasibility` falls with capital intensity (r ≈ −0.47) and rises with autonomy (r ≈ +0.66); no high-capital action scores "easy" in a weak comuna.
- **Known edge:** a few of the smallest comunas show 0 unaided actions — the *honorarios*-understatement caveat biting at the extreme.

## B9a. Coverage matrix — the gap dashboard

A per-action coverage matrix (`data/action_coverage_matrix.csv`, one row per action) records whether the action has a sector-specific municipal route, an award precedent, a BIP precedent, a cost benchmark and fund amounts, plus a `coverage_status`. The empty cells are the backlog. Headline gaps on the current run:

| Gap | Actions affected |
| --- | --- |
| No sector-specific municipal route (only broad cross-sector funds) | 26 / 102 |
| No BIP precedent | 25 / 102 |
| No award precedent | 75 / 102 (so **27 / 102 now have one**) |
| No cost benchmark | 21 / 102 |

Two structural findings. (1) Award precedent is now **multi-sector**: the CONAF, FPA and GCF award crosswalks lift precedent from the old afolu-only picture to 27 actions spanning afolu, energy/buildings, waste/water and transport. (2) *Any* municipal route still matches every action because broad funds (PMU, PMB) fit anything — which is why the matrix tracks a **sector-specific** route as the honest signal. By sector, industry is the systematic hole (no sector-specific city route, firm-facing CORFO instruments instead), and transportation has no sector-specific *municipal* route because its funds are operator-facing (the MTT actor mismatch), even though every transport action carries a BIP precedent. Fill order: tighten the action-to-fund match to sector + actor + instrument, curate `access_tier`, then fill industry/transport supply and fund amounts.

## B10. What the model can / cannot claim

**Can:** city archetype (coarse); action difficulty bucket; a 0–1 feasibility leg; named reachable funds + access barrier; funded precedent — each on a real join. **Cannot:** funding probability; comuna ranking; adequacy (amounts mostly missing); award odds (no outcome data); domain capacity from a generic professionalization proxy; real trends from nominal money.

## B11. Licence inheritance

Inherits the **most restrictive upstream licence**. Binding constraint: **SINIM** (non-commercial + attribution clear; commercial unresolved pending SUBDERE clearance). Finance sources add per-source terms (e.g. CORFO CC BY-NC-ND). Treat outputs as non-commercial + attribution until clearance lands; defer to each source review before redistributing.

## B12. Open items / next steps

1. **Curate `access_tier`** in the inventory — replace the "direct" substring heuristic with an explicit tier; detect the BIP/SNI gate (the real capacity barrier; B5 caveat).
2. **Action-actor inference** — read coverage against *who implements the action* (the industry/transport "gap" is an actor gap, not a supply gap). Biggest lever; gets action-level resolution.
3. **Revealed fundability** — mine award/adjudication history (what actually got funded, how often, at what size).
4. **Fill data gaps** — fund **amounts** (unlocks adequacy), more transport/industry supply, IPPU/AFOLU action coverage.
5. **Resolve the SINIM commercial licence** with SUBDERE.
6. **HIAP wiring** — fold `financial_feasibility` into the Feasibility pillar (needs Impact/Alignment from CityCatalyst to show real rank shift); weight sign-off by owner.

*Done:* harmonized inventory (99 funds, 10 sources); coverage indicator; four-layer model + full national run; multi-sector award precedent via CONAF/FPA/GCF crosswalks; the traceable `finance_db` fixture with explicit access routes; sensitivity validation.

## Inputs

`reviews/cl-ssg/cl-ssg-projects` · `reviews/cl-subdere/cl-subdere-sinim` · `reviews/cl-ine/cl-ine-censo` · the ten `cl-*/cl-*-fondos` supply reviews · CONAF/FPA/GCF award reviews (precedent) · `reviews/cl-ssg/cl-ssg-legal-signals` (validation only). Each remains authoritative for its own provenance, licence and caveats.
