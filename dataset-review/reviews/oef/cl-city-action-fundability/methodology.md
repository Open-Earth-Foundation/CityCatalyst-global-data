# How Chile city action financial feasibility works

A method for estimating, for a given Chilean municipality (*comuna*) and a given climate action, **how realistically the city can pay for and deliver it — and which funds could help**. It produces a 0–1 *financial feasibility* score with a plain-language reason and the named funds and past projects behind it. It is one input into the broader HIAP action-prioritisation tool (the **Feasibility** pillar).

---

## In one paragraph

Every climate action needs **money** and **know-how**. Every city has some **of its own money** and some **delivery capacity**. We compare the two: if an action's needs sit within what the city already has, it is *self-deliverable*; if not, we identify the gap (money, capacity, or both) and the **financing route** that closes it, then check **what funds actually exist** for that action's sector and whether the city can apply to them. The result is a score from 0 (very hard for this city to finance) to 1 (the city can do it with its own means), each one carrying the inputs that produced it so it is auditable, never a black box.

---

## What it answers — and what it doesn't

**It answers:** for one city and one action — how hard is this to fund and deliver, by what route, with which funds, and is there precedent? It is designed to *order actions within a single city* by financing difficulty and attach the supporting evidence.

**It does not:**

- predict whether an action will actually *secure* funding (it is not an award probability),
- rank cities against each other,
- lower an action's climate impact because a city is weak (a hard action in a weak city is *harder / needs outside help*, not *less worth doing*),
- judge whether a fund's amount is *enough* (amounts are sparse and mixed-unit; adequacy is not measured).

Read it as a **"how hard, and where to look"** map, not a funding guarantee.

---

## The four things we look at (the four layers)

| Layer | Plain meaning | Where it comes from |
|---|---|---|
| **Action** — *what* is being done | how much **money** it needs and how much **preparation** it takes | the climate-action library (C40 / IPCC / I-Care) |
| **City** — *who* would do it | how much **own money** and **delivery capacity** the city has | SUBDERE / SINIM municipal indicators |
| **Finance** — *the money* available | which catalogued **funds** match the action and whether the city can apply | the harmonised Chile finance inventory (10 public + firm-facing sources) |
| **Precedent** — *the evidence* | how many **comparable projects** have already been funded | BIP/SNI, plus CONAF, FPA and GCF award records |

The score is a **forward** comparison of the first three (Action × City → Finance). **Precedent** is shown as evidence alongside the score — it calibrates and illustrates, but is not fed back into the number (that would be circular).

---

## How the score is built — step by step

### 1. Size up the action — what it needs

Two needs, each on a 0–1 scale:

- **Capital intensity** — how much money the action needs.
- **Preparation complexity** — how much technical/administrative work it takes to turn the idea into a fundable project.

*The detail:* capital intensity comes from the action's investment-cost band (low / medium / high → 0.2 / 0.5 / 0.8). Preparation complexity comes from the action's type (a regulation is cheap to prepare → 0.2; planning / programme / financial → 0.5; building infrastructure → 0.8, or 0.9 if it's also high-cost).

### 2. Size up the city — what it has

Two strengths, each on a 0–1 scale, kept separate because they measure different things:

- **Financial autonomy** — how much of its budget the city raises itself rather than relying on central transfers. Higher = more of its own money to spend.
- **Delivery capacity** — the city's *internal capacity to develop and shepherd a project through to finance*: the professional staff who can write a proposal, formulate an *iniciativa*, pass the SNI/BIP gate, and manage a grant. **This is not the capacity to physically carry out the action itself** (build the plant, run the fleet) — it is the institutional capacity to turn an action into a funded project.

These two are not fully independent: capacity is partly what *unlocks* the finance. A fund existing is not the same as a city being able to reach it — many channels (e.g. the public-investment SNI/BIP route) are accessible only to a city with the staff to formulate and pass them. So readiness is, in part, the key to the money rather than a parallel, separate thing — which is why the score combines them rather than reporting two unrelated numbers.

*The detail:* autonomy = `1 − FCM-dependency%/100` (FCM is the central municipal-transfer fund). Capacity = a blend of two staff measures (`0.7 × percentile(professional staff) + 0.3 × percentile(professionalisation %)`). Both come from the 2025 SINIM data, for all 345 comunas, and both land on a 0–1 scale.

We also summarise the two into one **city profile** (a quick label), split at the midpoint of each axis:

| | High capacity | Lower capacity |
|---|---|---|
| **High autonomy** | **Self-sufficient** | **Well-resourced** (money, building capacity) |
| **Lower autonomy** | **Delivery-ready** (capable, cash-tight) | **Support-ready** |

The autonomy and capacity numbers are used *inside* the model to set the route; the API surfaces only this **city profile** category, not the underlying numbers.

### 3. Compare them → a financing route

Test each action need against the city strength it draws on — money-need against autonomy, preparation-need against capacity. Whichever falls short sets the **route**:

| | Low-capital action | High-capital action |
|---|---|---|
| **High autonomy** | self-deliverable | own-budget feasible |
| **Lower autonomy** | self-deliverable | needs external co-finance |

when an action's **preparation** need outstrips the city's **capacity**, the route escalates to *"+ technical assistance"*. The five routes, easiest to hardest:

1. **self-deliverable** — low-cost action the city can just do (e.g. a regulation),
2. **own-budget feasible** — within the city's own budget and capacity,
3. **needs technical assistance** — the city has the money but not the know-how,
4. **needs external co-finance** — the city needs outside money,
5. **needs external finance + TA / pooling** — it needs both outside money and outside expertise.

Low-cost actions look the same for every city (money isn't the constraint); demanding actions are where cities diverge.

### 4. Check what money is available

For the action's sector, look up the **finance inventory** and ask: are there funds the city can reach? We classify the access into one of three:

- **direct** — there is a catalogued fund the city can apply to itself,
- **competitive** — funding exists, but it is won through a competition (*concurso*),
- **gap** — no catalogued fund matches this sector yet.

*Why access matters:* the same fund can be "reachable" for a capable city and "needs help to access" for a weaker one — a direct-application grant is open to anyone, while a fund routed through the national investment system (the BIP/SNI gate) demands more capacity to unlock.

### 5. Turn it into a 0–1 score

The route, combined with how reachable the money is, maps to the feasibility score:

| Situation | Score |
|---|---|
| self-deliverable | **1.00** |
| own-budget feasible | **0.85** |
| needs technical assistance | **0.70** |
| needs co-finance — a direct fund exists | **0.60** |
| needs co-finance — only competitive funding | **0.45** |
| needs co-finance — no catalogued fund (gap) | **0.25** |
| needs finance **and** technical assistance | **0.15–0.35** (by fund access) |
| no city data available | **0.50** (neutral fallback) |

Higher = the city can more readily finance and deliver the action. The bands are deliberate, tunable settings — not statistical estimates.

*Why a money gap scores lower than a capacity gap* (e.g. *gap* 0.25 vs *needs technical assistance* 0.70): the model isn't saying money matters more in principle — it reflects that **a money gap is harder to close than a know-how gap**. A capacity gap can be bought in (technical assistance is comparatively cheap and available, and the project still moves), whereas a capital gap with no catalogued fund is closer to a hard stop — without funding a capital project doesn't happen, and if no fund exists there's no route to one. So the ordering encodes "how resolvable is the binding constraint," not "which input is more important." Because the bands are tunable, this can be revisited if the team weighs the two differently — and note the *gap* score partly reflects what we have catalogued (an availability bias), so it may read harsher than reality in under-reviewed sectors.

### 6. Attach the evidence

Finally, count the **comparable projects already on record** for the action (from the precedent layer) and surface the matched funds. These don't change the score — they let a reader see that the route is real ("57 similar projects have been funded") rather than taking the number on faith.

---

## A worked example

**Valdivia** is *Delivery-ready*: lower financial autonomy (it leans on central transfers) but strong delivery capacity.

- *"Introduce energy-efficiency standards for new buildings"* — a low-capital **regulation**. It needs little money and little preparation, both within Valdivia's reach → **self-deliverable, score 1.00**. Reason: *"Low-capital action the city can deliver itself."*
- *"Retrofit municipal buildings for energy efficiency"* — **high-capital** infrastructure. Valdivia can manage the delivery, but the capital exceeds its own-money headroom → **needs external co-finance**; energy-sector funds exist that the city can apply to → **score 0.60**. Reason: *"Capital need exceeds the city's autonomy; co-finance available via 3 fund(s) the city can apply to directly."*

Same city, same staff — the difference is the *action's* demands meeting the *city's* means.

---

## Where the data comes from

| Layer | Source review(s) |
|---|---|
| Action demands | the OpenEarth / SSG climate-action library (`cl-ssg-actions`, served via `action_pathway`) |
| City axes | SUBDERE / SINIM municipal fiscal & staffing indicators (`cl-subdere-sinim`), with census/SSG context |
| Finance | the ten `cl-*` *fondos* supply reviews, harmonised into one fund inventory |
| Precedent | BIP/SNI projects (`cl-ssg-projects`) plus CONAF, FPA and GCF award records |
| City identity | comuna → city locode via the `cl-ocha-ab` administrative-boundary lookup |

Each source review remains authoritative for its own provenance, licence and caveats; this product unions and scores already-reviewed data and re-grants nothing.

---

## A companion view: the coverage / gap map

Alongside the per-city score there is a national **coverage indicator** — a simpler, city-agnostic answer to *"does a dedicated, currently-usable, city-accessible fund exist for this action's sector?"* It labels each action `sector-specific` (a dedicated municipal fund exists), `broad-only` (only general-purpose funds), or `none`. It is an honest **gap dashboard** (which sectors lack dedicated city funding), not a per-action score — and it carries an **availability bias**: well-reviewed sectors light up, under-reviewed ones look like gaps regardless of reality. Its standout finding: the apparent "gaps" in industry and transport are mostly an **actor gap, not a money gap** — cities don't run bus fleets or decarbonise factories; firms and operators do.

---

## Action-to-opportunity matching (v2, working)

*Working methodology for the v2 release. It replaces the sector-level matching that produced the v1 draft links, and it is not yet reflected in the production tables.*

The organising principle is that **how specifically a fund matches an action follows from how specific the fund is.** A fund written for a purpose, such as native forest conservation, matches a few actions closely. A fund written for a class of works, such as a municipal capital transfer, matches many actions loosely, and that is what the fund *is* rather than a defect in the matching. Most of the match type is therefore derived from the route rather than assigned by hand.

Three properties of the fund and one of the action drive the derivation. From the fund: how targeted the route is, what the money buys, and whether a municipality can receive it. From the action: what it takes to deliver, which is the question of who owns the thing that changes. If the asset or the practice belongs to a firm, a farmer or a household, the city can enable it but cannot buy it.

The five match types follow, and only two of them are ever assigned by a person.

| Match type | Meaning | Assigned how | Counts as coverage |
|---|---|---|---|
| `whole` | The fund's purpose is this action. | Reviewed | Yes, if the city can apply |
| `part` | The fund finances a material piece of it. | Reviewed | Yes, if the city can apply |
| `prepares` | The fund buys planning, capacity or access, never the asset. | Pair reviewed, type forced by what the fund buys | No |
| `general_route` | A general municipal fund covers this class of activity. | Derived from route, money and delivery mode | No |
| `none` | Nothing matched. | Derived | No |

Coverage needs both halves: a relationship strong enough to finance the action, and a municipality able to receive the money. A reviewed link can name a fund that finances an action while the city has no way to apply, and that link is kept rather than deleted, marked as not city-applicable. Deleting it would hide the most decision-relevant pattern in the data, that for many actions the money exists in Chile and is directed at someone other than the city.

Availability is a third, separate gate. A link is shown by default only when it counts as coverage, the opportunity's status, dates, geography and eligible applicant are all evidenced, and the municipality and applicant checks pass at request time. Records that are unknown, closed, revoked, programme-only or regionally unsplit stay in the data and are suppressed from display, because the relationship holds even while the call does not.

The crosswalk records two axes rather than one. `covers` holds the scope of the relationship, whole or part, and `mapping_confidence` holds how well established it is, as high, medium or none. This splits the house mapping schema's single confidence column in two because scope and certainty are independent here: a fund can certainly finance part of an action, or uncertainly finance all of it. A fund that was reviewed and matched nothing is kept as a row with `covers` and `mapping_confidence` both `none`, which is the record that stops the next reviewer repeating the work. Every reviewed row carries a rationale, its outstanding verification, and the adjudicator and date; derived rows carry no confidence, because their basis is the rule itself.

The absence of a link means only that no relationship has been established from the evidence read so far. It is not proof that future or regional calls can never support the action, and coverage grows by verifying more funds in the compile rather than by widening the match rules.

### References

- curated crosswalk, the only stored judgement → `releases/v2/data/action_opportunity_mapping.csv`
- action delivery modes → `releases/v2/data/action_delivery_mode.csv`
- route profile on each fund → `dataset-compile/cl-climate-finance-opportunities/data.csv`
- resolved links with display gating → `releases/v2/data/finance_opportunity_action.csv`
- build and validation → `releases/v2/01_opportunity_action_links.ipynb`

---

## What it can and cannot claim

**Can:** a coarse city profile; an action's difficulty route; a 0–1 feasibility score with a plain reason; the named, reachable funds and how to access them; funded precedent — each built on a real data join.

**Cannot:** a probability of getting funded; a ranking of cities; whether a fund's amount is *enough*; award odds (no outcome data is used); deep sector-specific capacity (the staff measure is general); real spending trends (amounts are nominal and sparse).

---

## How it feeds the bigger picture

The score plugs into HIAP's **Feasibility** pillar as a third leg alongside legal and mitigation feasibility (proposed weights legal 0.34 / mitigation 0.33 / financial 0.33). Because Feasibility is only part of the overall HIAP score, financial feasibility is a small share of the total — enough to break ties and nudge prioritisation, never enough to swamp an action's climate impact. The highest-value output is the **annotation** (route + funds + precedent + reason), not the bare number. Weight changes need methodology-owner sign-off.

---

## Status and what's next

**Implemented in production.** The model is built end to end: the inputs live as database tables (`finance_opportunity`, `finance_project`, `city_finance_profile` and their action links), the score is computed at read time by the `city_action_financial_feasibility` function (so it's always current and never stale), and it's served by the `climate-finance` API (the score, a per-action drill-down, the fund catalogue, and the precedent projects). See `releases/v1/implementation.md` for the technical shape.

**Action matching is being rebuilt (v2, research).** The v2 release derives the match from the route rather than asserting it pair by pair (see *Action-to-opportunity matching* above), and separates coverage, city eligibility and current availability into three gates. Of 102 actions, 11 are covered by a fund a city can apply to, 18 have a general municipal route, 48 are funded in the territory but not for the city, and 25 have nothing, none of which needs capital. It is not production-approved and has not been loaded into the modelled tables.

**Honest limitations / next steps:**

1. **Fund access is a rough flag today.** "direct vs competitive" is a simple text heuristic and does not yet detect the BIP/SNI capacity gate. The fix is a curated *access tier* — the single biggest quality improvement.
2. **Action-actor inference** — read coverage against *who implements the action*, to resolve the industry/transport "gaps."
3. **Revealed fundability** — mine real award history (what actually got funded, how often, at what size).
4. **Fill data gaps** — fund amounts (to unlock adequacy), more transport/industry supply.
5. **Confirm SINIM terms with SUBDERE *only before any commercial use*** — not a blocker today (see Licence).

---

## Licence

Inherits the **most restrictive upstream licence**; the binding constraint is **SINIM** (non-commercial + attribution clear). **We use SINIM as a derived model input, not a redistribution:** the published outputs are computed scores (`autonomy`, `capacity`, `city_archetype`) — the raw SINIM indicators are consumed in the transform and not stored or served. With attribution to SUBDERE/SINIM maintained, the current **non-commercial** research / tool use is in the clear. The one open question is narrower — a non-commercial term can carry to derivative works, so **commercial use of the product would still warrant a confirmation with SUBDERE**. Some finance sources add their own terms (e.g. CORFO `CC BY-NC-ND`); defer to each source review before redistributing any raw data. *(Not legal advice — confirm with the licence owner.)*
