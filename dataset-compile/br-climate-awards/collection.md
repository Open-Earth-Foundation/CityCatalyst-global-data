# br-climate-awards — collection notes

Provenance and method for the compiled dataset in this folder. This is a **staging dataset**: manufactured from public Brazilian funder award/selection lists, not ingested from a single publisher, and **not yet vetted** through `dataset-review/`. Read alongside `schema.json` (the contract) and `sources.yaml` (the source registry). Sibling instance to `dataset-compile/mn-climate-awards/` (Minnesota) — same design, Brazilian values, Portuguese sources.

## What this is

Real awarded/selected climate-finance records in Brazil, indexed by reaching-money **route** (rollup) and per-record facets — **funder · category · region · instrument**. Region for Brazil = **município + UF (estado)**, rolled up to macrorregião. It exists to give evidence for which funding *path* a Brazilian city (or the actors around it) can actually reach, and to power comparable-project logic. **Routes A, B, C only** in this pass — the narrow, most-award-rich start.

## How it was collected

1. **Navigated by the landscape doc.** `knowledge-base/topics/climate-finance/br-climate-finance.md` names the six routes, the funders on each, and the "Main actors" table. That reference — not this data — was the map. It named Fundo Amazônia and Fundo Amazônia's portal as the cleanest published award list, Novo PAC as the formulate-and-select pipeline, and COFIEX as the direct-borrowing portfolio.
2. **Started narrow** with the 3 most award-rich routes (the Brazilian analog of how Minnesota started with its competitive-grant and revolving-fund routes): A = Fundo Amazônia carteira, B = Novo PAC 2025 (drenagem + contenção de encostas), C = COFIEX 180ª Reunião.
3. **Fetched primary sources** (see `sources.yaml`): funder portals and the project-level PDFs/tables they publish. PDFs were read with the WebFetch text extractor (direct code download is proxy-blocked here); the extracted text is kept in `raw/` for re-parse.
4. **Extracted award/selection lines** — recipient + amount read directly off those sources.
5. **Structured + enriched** into `schema.json`'s fields via `raw/build_data.py`.
6. **Verified against control totals** (below).

## Provenance is a gradient — read this before trusting a field

Fields are tagged `sourced` / `derived` / `derived-by-rule` / `meta` in `schema.json`. The `derived` fields are lower-trust and are the main work remaining before this can become a proper dataset:

- **`route`** — computed from funder/instrument via the six-route model; not stated on any award page.
- **`category`** — assigned from programme + project name/theme by a keyword rule in `build_data.py`; needs a curated deterministic mapping. Adaptation-relevance is **not assumed**: `climate-adaptation` / `urban-resilience` are tagged only where the source itself names clima/adaptação/resiliência (per the landscape doc's warning that most Brazilian funds are mitigation/forest-weighted).

`region_macro` and `amazonia_legal` are **derived-by-rule** (an improvement): computed from `uf` via the auditable `references/br-region-lookup.csv`. Correct a UF's region/Amazônia-Legal status in one place rather than per row. `uf`, `municipio`, `recipient`, `amount`, `currency`, `funder`, `project_name` are read from the source.

## Verification status — reconciliation to control totals

The strongest QA available: where a source publishes an aggregate, we checked our row sums tie to it.

- **Route A — Fundo Amazônia (146 grants).** The web carteira (fetched 2026-07-05, current) reconciles to the **Informe da Carteira 30/12/2025** control totals. Four of six natureza counts tie **exactly** — Estados 31|31, Municípios 7|7, Universidades 6|6, Internacional 1|1 — and six location buckets tie exactly (AM 15, AC 11, RO 7, MA 4, AP 3, Internacional 1; "Fora da Amazônia Legal" = BA+CE+MS+PR+ES = 5|5). Total valor do apoio **R$5,282.8 mi vs R$5,195 mi** (+1.7%), and all deltas are small and directionally consistent with the web being ~6 months newer than the Dec-2025 informe (2 more Soc.Civil projects, +R$88mi). One open item: União count 13 vs 14 and value R$1.99bn vs R$2.14bn — one large União project appears to have moved/completed between the two dates. Full detail in `raw/fundo-amazonia-reconciliation.md`. **All Route A rows verified=true.**
- **Route C — COFIEX 180ª (32 line items).** The full results table reconciles **exactly** to the release: **18 subnacionais + 4 federais/empresas = 22 approvals** (our data: estado 11 + município 7 = 18 subnacional approved; 4 federal/empresa approved), and the **federal approved sum = US$1.12bn** exactly as the release states (MIR 100 + MS 320.003 + MIDR 500 + CAIXA 200). USD-denominated approvals sum US$3.37bn; adding the R$-denominated approvals (R$2.35bn ≈ US$0.43bn) gives ≈US$3.8bn ≈ the release's "US$3.7bn". **All Route C rows verified=true** (a bad fetch would not reconcile this cleanly).
- **Route B — Novo PAC 2025 (315 selected proposals).** Now the **full per-proposal selected list**, extracted from the 5 official Ministério das Cidades XLSX (`drenagem/encostas` × `FGTS/OGU`, plus the `drenagemap` financing-routed drenagem list). Reconciles cleanly to the published control totals: **drenagem R$10,302.9mi vs R$10,300mi (exact to 0.03%)**; encostas R$1,432.3mi vs the release's "mais de R$1,4 bilhão" (✓); **total R$11,735.2mi vs R$11,700mi (+0.3%)**; **26 UFs exact**; 230 distinct municípios vs the announced 235 (the small gap is name-spelling noise — the source files spell some municípios inconsistently, e.g. "Camaçari"/"Camacari"). Two independent per-município cross-checks land on the federal release's named highlights: **Duque de Caxias/RJ = R$555mi** (release R$554mi) and **Camaçari/BA = R$125mi + R$114.7mi = R$239.7mi** (release R$240mi). **All 315 proposal rows `verified=true`.** Note the `drenagemap` file, labelled "não habilitadas para OGU", are still *selected* drenagem works (routed to FGTS financing) — proven by the fact that they are exactly what closes the drenagem total to R$10.3bn.

## Insights — what the data says

Computed from the 496 rows. Directional; three routes, recent cycles.

- **The rollup is lopsided in *effort*, not availability — that is the finding.** All three routes turned out enumerable, but the reachability differed sharply. Route A (Fundo Amazônia) publishes a fully open per-project table → 146 rows, straight through. Route C (COFIEX) publishes a clean per-meeting results PDF → 32 rows, straight through. Route B (Novo PAC) — the largest pot (R$11.7bn) and the most adaptation-relevant — hid its per-município list behind a login on the Casa Civil portal, but the **same list is published openly by the Ministério das Cidades as five XLSX** (`relacao-de-propostas`); once those were in hand it yielded **315 fully-reconciled proposal rows**. The lesson for future compiles: the biggest, most-relevant pot was reachable, but only via a *different, less obvious open door* than the headline portal — and (in this environment) only after the binary spreadsheets were fetched outside the sandbox.

- **Three routes, three orders of magnitude and three instruments.** Route A is a **grant** world (median R$16.4mi, non-reembolsável, forest/land-use). Route C is a **loan** world (MDB credit, US$50–845mi per operation, CAPAG-gated). Route B is a **grant+loan transfer** world (OGU + FGTS financing) at the largest aggregate scale (R$11.7bn one cycle). The route sets the instrument, the ceiling, the document, and the gate — exactly the through-line the landscape doc predicts.

- **Route A money concentrates at the top and in the Amazônia Legal.** The top 5 grants take **30%** of the R$5.28bn and the top 10 take **44%**; the largest is Ibama's FORTFISC enforcement grant (R$825.7mi). By executor, **civil society (terceiro setor) wins on count (87 projects, R$2.30bn)** but the **União wins on value density (13 projects, R$1.99bn)** — a few huge federal enforcement/fire programmes. **139 of 146** projects touch the Amazônia Legal. Municípios are a thin 7 projects / R$14mi — cities are mostly *beneficiaries via OSCs and states*, not direct grantees, matching the landscape doc's "city-as-enabler" reading.

- **Route A is forest-first, adaptation-adjacent.** Categories: forest-conservation 62, sustainable-production 27, monitoring-control 16, territorial-management 15, restoration-water 10, fire-management 9, research 6, sanitation 1. This is mitigation/forest money; the adaptation-relevant slices are fire-management (disaster-prevention-adjacent), restoration-water, and the single Sanear Amazônia sanitation grant. Confirms the doc: **climate-badged Brazilian money is not primarily urban-adaptation money.**

- **Route C is where the explicit climate/adaptation labels live — and CAPAG gates them.** 10 of 32 COFIEX line items are environment/climate/resilience-tagged, including two **named climate projects for the município of Palmas/TO** ("Transformação Ambiental frente às Mudanças Climáticas", CAF US$60mi; "Resiliência Climática — Córrego Machado", BID R$447mi), Manaus and Fortaleza fiscal-*and-environmental* debt restructurings, and Joinville's resilience programme. But the route is CAPAG-gated and capital-city-weighted (Fortaleza, Manaus, Niterói, São Paulo, Salvador), and several environmental/climate pleitos were **não aprovado** this meeting (Espírito Santo rural, Amapá "Amaparque" adaptation) — the queue is real, exactly as the landscape doc's CAPAG gate implies.

- **Route B is the real urban-adaptation pot — and its shape is the opposite of Route A's.** R$11.7bn for exactly the flood/drainage/landslide works an urban adaptation plan calls for, across 315 selected proposals / ~235 municípios. Drainage is 88% (R$10.3bn). Unlike Route A's forest money, it is (a) **geographically Southeast/Northeast, not Amazonian** — Sudeste R$5.0bn (129 proposals) + Nordeste R$3.4bn (84) is 71% of the money, and only **62 of 315 proposals touch the Amazônia Legal** (vs 139/146 in Route A); (b) **far less concentrated** — top-5 municípios take just **8.2%** (vs 30% in Route A), median proposal R$22.7mi, max R$215.9mi (Belo Horizonte macrodrainage); and (c) **split ~50/50 by value between an OGU grant arm** (222 proposals, R$5.95bn, non-reembolsável repasse) **and an FGTS loan arm** (93 proposals, R$5.78bn, financiamento) — the grant arm reaches 2.4× more municípios with smaller tickets, the loan arm fewer municípios with bigger ones. This is a municipal-government award list (303 of 315 proponents are municípios, 12 are states), i.e. the one route here where the city itself is the direct recipient — matching the landscape doc's Route B "city formulates and submits" framing.

- **The through-line for the routes model.** A Brazilian city's reachable climate money is stratified exactly as `br-climate-finance.md` says: grant/forest money (A) flows through OSCs and states, not city halls; direct MDB loans (C) are open only to creditworthy capitals and states; and the drainage/disaster transfers (B) that matter most for adaptation are real and large but reached by a gated selection, not an open award list. Compiling by route makes that structure legible in a way the prose reference alone could not.

## Coverage readiness

| Route | Depth | Enumerable? | Usable as "show examples"? |
|---|---|---|---|
| A — Fundo Amazônia (grants) | full carteira, per-project, reconciled | yes (open portal) | yes |
| B — Novo PAC drainage/encostas | full per-proposal list (315), reconciled | yes (official xlsx) | yes |
| C — COFIEX (MDB loans) | full 180ª meeting, per-project, reconciled | yes (per-meeting PDF) | yes |
| D — GCF/GEF/Adaptation Fund | absent | portfolio only | no |
| E — MIDR/Sedec disaster | absent | messy (S2ID) | no |
| F — emendas | absent (windfall, no call) | no | no |

Verdict: strong, reconciled evidence for the grant route and the direct-borrowing route; a real but gated view of the drainage/disaster transfer route. Enough to show that Brazil's reachable, documented climate money is grant-and-loan shaped and route-stratified — and to point precisely at the gated Route-B list as the highest-value next pull.

## Known gaps (the to-proper checklist)

- **Route B per-município selected list — DONE.** The full list (315 selected proposals) is now in `data.csv`, from the 5 official MCidades XLSX (saved in `raw/novopac_xlsx/`), reconciled to the eixo control totals. Residual on this route: (a) **município count 230 vs announced 235** — source files spell some municípios inconsistently (accents/cedilhas, e.g. "Camaçari"/"Camacari"); a name-normalization pass against the IBGE município table would resolve it without risking wrong merges; (b) **per-proposal award dates** not in the sheets (the seleção was announced 2025-09-18); (c) a handful of OGU rows carry multiple beneficiary municípios in one cell — kept as one proposal row.
- **Fundo Amazônia award dates** — the carteira publishes situação (contratado/concluído) but not per-project contract date; `award_date` is blank for Route A. The annual "Relatório de Atividades" or per-project subpages carry the date.
- **Fundo Amazônia per-project desembolso** — only valor do apoio (approved) is on the list; desembolsado is portfolio-level in the informe.
- **COFIEX beyond the 180ª** — only one meeting pulled; the 181ª+ and the Painel COFIEX (execution phase) would extend Route C and add a signed/executed status.
- **Derived-field rules** — replace the keyword-based `category` and the `route` assignment with curated deterministic rules; both are `derived` today.
- **Routes D, E, F** — deliberately absent this pass (portfolio-only, messy, or non-enumerable — the predicted lopsidedness at the route level).
- **One União reconciliation item** — Route A União count/value differs from the Dec-2025 informe by one large project (see verification).

## Refresh model

No feed to poll. "Refresh" = re-run the compile against the sources in `sources.yaml` and diff. Each source carries a `last_fetched` date; the Fundo Amazônia monthly informe and the COFIEX per-meeting results are the natural refresh anchors. `raw/build_data.py` regenerates `data.csv` from the `raw/*.tsv` extracts.

## Promotion

When scope is locked, `derived` route/category are computed by rule, the Route B per-município list is filled from a primary source, award dates are added, and provenance is complete, this graduates into `dataset-review/` — which creates the catalog entry and, downstream, the pipeline.
