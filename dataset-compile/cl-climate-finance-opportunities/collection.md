# cl-climate-finance-opportunities — collection notes

Provenance and method for a compiled staging dataset of Chilean climate-finance
opportunities. It is manufactured from scattered official sources, is not an
external publisher dataset, and is **not yet vetted for production use**.

## What this is

The compile preserves all 99 records from the reviewed Chile finance inventory
and progressively resolves them into programme families, application calls,
regional variants, public-investment routes and enabling platforms. Its purpose
is to retain potentially useful opportunities without presenting stale,
ineligible or weakly evidenced records as current action-level funding.

The intended query is: for a Chilean municipality and climate action, which
currently evidenced calls, recurring programmes, public-investment routes or
enabling supports may be relevant, and what primary evidence establishes their
activity, asset, applicant, geography and timing?

## How it was collected

1. Seeded all 99 rows from
   `dataset-review/reviews/oef/cl-city-action-fundability/releases/v1/data/chile_finance_inventory.csv`.
2. Preserved every seed claim verbatim; new status fields are separate.
3. Registered every distinct seed URL in `sources.yaml`, initially with a null
   `last_fetched` date unless checked in this compile.
4. Checked an initial cross-funder batch against official programme pages, call
   pages, bases, budget documents and government application indexes.
5. Applied checked conclusions through the auditable exact-name table
   `references/verified-record-overrides.csv`.
6. Ran `validate.py` to prove lossless seed retention and prevent unverified
   rows from acquiring a normalized status or display eligibility.
7. Derived the route profile (see below) from source-stated values through the
   exact-match lookups in `references/applicant-class-map.csv` and
   `references/funding-mode-map.csv`, with per-programme exceptions recorded in
   `references/route-profile-overrides.csv`.

## Provenance is a gradient

- The 99 original values remain `sourced` claims inherited from the reviewed
  inventory. `verification_status=seed_not_reverified` means this compile has
  not independently re-read the primary source.
- `record_scope` is deliberately `seed_unspecified` until evidence establishes
  whether the record is a programme, call, route or platform.
- Programme-family and normalized-status assignments are applied only through
  `references/verified-record-overrides.csv`.
- `current_display_eligible` remains false for every row. This compile is a
  research layer, not a production display feed.

No missing source fact is filled by plausibility. Unknown values remain blank
or `unknown`; inaccessible or conflicting pages are recorded as such.

## Verification status — 2026-08-16

- 99/99 seed records preserved, plus 1 newly discovered current call.
- 14 records checked against current primary evidence in the first research batches.
- 86 records remain seed-only and must not be treated as reverified.
- 105 sources registered, including official supporting documents that are not
  themselves seed rows.
- 0 records marked display-eligible.

| Source family | Seed records | Reverified in compile | Status |
|---|---:|---:|---|
| CONAF | 2 | 1 | Partial; 2026 conservation call identified separately from stale 2025 seed URL |
| CORFO | 5 | 0 | Pending; seed Crédito Verde page was not fetchable in this pass |
| GORE | 4 | 2 | Partial; FNDR route confirmed, FRIL source conflict found |
| INDAP | 9 | 1 | Partial; TAS programme checked, current window year not inferred |
| Energy / AgenciaSE | 6 | 2 | Partial; platform and rollout distinguished from live calls |
| MINVU | 4 | 2 | Partial; programme mechanisms checked, current regional calls pending |
| MMA | 55 | 2 | FPR 2026 found revoked; one new current Lo Espejo call added; remaining family work pending |
| MOP | 7 | 1 | Partial; SSR confirmed as investment route rather than open municipal grant |
| MTT / DTPR | 3 | 1 | Partial; Renueva tu Colectivo requires regional-call expansion |
| SUBDERE | 4 | 2 | Partial; PMU and PMB active programme pages checked |

## The route profile

Five fields describe the route itself, so that downstream matching can be derived rather than hand-assigned. The design principle is that how specifically a fund matches an action follows from how specific the fund is: a targeted route can support a specific action match, a general route can only support a general one, and a route that buys readiness can never support a capital claim at all.

- `route_scope` (targeted, general): normalised from the seed's specificity claim.
- `funds_what` (asset, equipment, practice, preparation, credit): what the money buys, by exact lookup on the instrument.
- `applicant_class`: who the money is actually for.
- `municipality_eligible` (yes, no, implementer, unknown): whether a municipality can receive it, kept separate from the class because the two genuinely diverge.
- `themes_norm`: the seed's sector tags mapped onto the action-sector vocabulary.

Two derivations are worth stating explicitly. Applicant class and city eligibility are separate because a municipality that owns forest land can apply to a landowner fund on the same footing as any other landowner, while in a producer programme delivered through a municipal convenio the city implements without ever receiving the money; that second case is recorded as `implementer`. And an enabling platform is treated as funding preparation whatever its nominal instrument mix says, because a mixed grant-and-advice instrument would otherwise read as capital.

Everything derives from exact-match lookups in `references/`, never from per-row judgment or keyword guessing, and `validate.py` asserts that every value in the data resolves through a lookup row and that no lookup row is unused. Nothing is filled by plausibility: the 29 records whose seed recorded no applicant map to `unknown` rather than inheriting their programme family's usual applicant.

### What the profile shows

| Cut | Result |
|---|---|
| Routes a municipality can receive | 27 of 100 |
| Not for municipalities | 42 |
| City eligibility unknown | 29 |
| City implements but does not receive | 2 |
| Targeted / general | 80 / 20 |
| Buys an asset | 77 |
| Buys practice change, equipment, preparation or credit | 9, 5, 5, 4 |

The 27 city-receivable routes are the real municipal opportunity set, and it is a quarter of the inventory. The 42 marked not-for-municipalities are the actor gap made countable: the money exists in the territory, but a city cannot apply for it.

## Findings from the verified batch

1. **The seed mixes different grains.** FPR 2026 is a national call, Comuna
   Energética is an enabling platform, FNDR/SNI is a public-investment route,
   and Renueva tu Colectivo is a programme implemented through regional calls.
2. **Current status cannot be inherited safely.** The seed's CONAF source points
   to a 2025 call while a separate 2026 call existed and closed on 31 July 2026.
   The FPR 2026 page now links a resolution leaving that call without effect.
3. **Programme pages are not call evidence.** The MINVU Espacios Públicos page
   still presents a 2023-2024 call, so current availability remains unknown.
4. **Some source links do not support the named record.** The FRIL seed link is
   a general Gobierno de Santiago regional-investment/FNDR page, not evidence
   for a current FRIL call.
5. **Municipal relevance is not municipal eligibility.** TAS is directed to
   eligible INDAP users; SSR investment centres rural service operators; forest
   conservation calls target landowners. These may support municipal climate
   outcomes without being municipal grants.
6. **New opportunities can be added without erasing history.** The official MMA
   portal exposed a Parque Landaeta call open from 21 July to 15 September 2026,
   absent from the seed. It is stored as a new local call with its stated Lo
   Espejo territory, CLP 95 million amount and non-municipal applicant classes.

## Known gaps and next research batches

- Split recurring national programmes into dated calls and retain historic calls.
- Extract all 2026 Renueva tu Colectivo and Renueva tu Micro regional processes.
- Check FRIL, regional environmental subsidies and FRPD across all 16 GOREs.
- Resolve CORFO pages and distinguish intermediary credit facilities from grants.
- Review all current MMA/FPA/FPR family pages and cancellation/adjudication acts.
- Capture the 59-comuna Parque Solar Comunitario geography as an auditable lookup.
- Split MINVU Parques Urbanos into SEREMI-prioritised construction and municipal
  conservation calls.
- Add structured eligible activities, assets, exclusions, costs and geography
  only from call bases or equivalent primary documents.
- Create a separate post-seed call layer before marking any record currently usable.
- Resolve the applicant for the 29 records whose seed recorded none. All 29 are historic FPA calls from 2020 to 2025, and the FPA bases state applicant types, so this is a bounded fetch rather than open research. Until it lands, city eligibility is unknown for those records and they cannot be counted either way.
- Resolve `cross_sector` on the 46 records still carrying it. It is retained rather than replaced by a guessed list, and `funds_what` plus `municipality_eligible` currently do the constraining work in its place, so this is a precision improvement rather than a correctness fix.
- Record the works class a general municipal fund covers. Buildings, public space, paving and basic services behave differently, and `funds_what: asset` is currently one bucket for all of them, which leaves a general fund reaching more actions than it should.

## Refresh model

There is no single upstream feed. Refresh means re-fetching `sources.yaml`,
diffing source state, adding new calls rather than overwriting historic ones,
and rerunning `build_seed.py` plus `validate.py`.

## Promotion

Promotion to `dataset-review` requires completion of the declared search scope,
programme/call separation, source-backed normalization, all 16 GORE checks,
peer review and a documented downstream display rule. Until then, the compile
must not be used as production truth.
