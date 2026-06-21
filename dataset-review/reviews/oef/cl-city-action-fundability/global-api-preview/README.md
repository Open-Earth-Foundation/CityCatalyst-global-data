# Global-API preview — Chile climate finance

A **working preview** of the design in `../global-api-database-design.md`, built from the real v1 `finance_db` fixture so the data shapes are visible *before* any migration or technical build. Nothing here is production code — it is a SQLite stand-in plus sample API responses.

## What's here

| File | What it is |
|---|---|
| `finance_preview.db` | SQLite DB with the proposed tables populated from the fixture: `finance_opportunity` (100), `finance_project` (11,310), `finance_action` (**view**, 102), `city_finance_profile` (345) |
| `schema.sql` | the `CREATE TABLE` / `CREATE VIEW` statements |
| `example_1_feasibility.json` | `GET …/climate-finance/feasibility` — per-action scores with the full `inputs` breakdown |
| `example_2_opportunities.json` | `GET …/climate-finance/opportunities?action_id=…` — reachable funds (reference) |
| `example_3_projects.json` | `GET …/climate-finance/projects?action_id=…` — precedent projects (reference) |
| `example_4_action_detail.json` | `GET …/climate-finance/actions/{action_id}` — composed drill-down (now includes `channels`) |
| `example_5_channels.json` | the `channels` block contrasted across two actions — shows public investment surfacing as an **evidenced** route, not a gap |
| `build_preview.py` / `generate_examples.py` | the scripts that build the DB and emit the JSON |

Demo city: **Iquique (CUT 01101)**. Focus action in examples 2–4: **`icare_0040` — solar-powered street lighting** (stationary_energy).

## What the preview confirms about the design

- **The score is derived, not stored.** `feasibility` carries every input under `inputs` (action demands · city axes · finance resolution · evidence) plus a plain-language `reason`. No score table exists.
- **`finance_action` works as a view.** Demands are banded from action attributes (`intervention_type` → `preparation_complexity`; `investment_cost` → `capital_intensity`) and benchmarks roll up from `finance_project` — e.g. street lighting gets a `cost_median_mmclp = 89.6` from 115 strong matches, with `duration` null (BIP durations are sparse).
- **The renamed/cleaned fields read well.** `city_application` (direct/facilitated/intermediated) and `funding_channel` (descriptor, no Route A/B/C) are populated; `open_date`/`close_date`/`amount_clp` come through.
- **Co-finance folds into JSON.** Each project's `funding_sources` array shows its sources (e.g. `F.N.D.R.` → the FNDR opportunity), confirming the link table isn't needed for v1.
- **Reachable funds split sector-specific vs broad.** For street lighting Iquique sees 8 sector-specific + 38 broad reachable funds — the broad cross-sector funds are surfaced but flagged, matching the methodology's "broad ≠ dedicated" rule.
- **Public investment is now an evidenced channel, not a gap (`example_5`).** `access_tier` is added to `finance_opportunity` and the feeder funds (FNDR, FRIL, PMU, PMB, PMR, FRC, FRPD) are re-tagged `funding_channel = public investment`, `access_tier = BIP-SNI-gated`. The `channels` block then drives public-investment availability off **BIP precedent**: zero-emission buses (a transport action with no sector-specific competitive municipal fund — `n_sector_specific = 0`) still shows `public_investment.available = true` via 11 FNDR-funded projects, so `is_real_gap = false`. Street lighting shows 114 FNDR-funded precedent the same way.

## Known preview limitations (not design problems)

1. **Dates on only 6 of 100 opportunities.** The fixture's `opportunities.csv` dropped dates; the preview re-joins them from `chile_finance_inventory.csv` by name, which only matched the 6 MMA/FPA funds. In production the loader carries `open_date`/`close_date`/`amount_clp` straight from the inventory source — coverage will be full where the source has them.
2. **`actor_id` is a placeholder** (`CL-COMUNA-<cut>`). The real CUT→actor_id lookup (Amanda's) replaces it at load.
3. **`n_existing_projects` (288) ≠ benchmark `n_projects` (115).** The score's count (from the methodology run) is looser than the strong/goal_aligned benchmark roll-up — a definition to align in the loader.
4. **`match_confidence` here is the dominant project-match label** (29 actions), a slightly looser cut than the methodology's stricter 21 `strong`. Use the methodology's grade in production.
5. **Score/route are taken from the methodology run** for display; the production endpoint computes the route bucket from the four input layers (the preview already computes the finance match and precedent live from the tables).
6. **`funding_channel` / `access_tier` are re-derived by a name/source heuristic** (`classify()` in `build_preview.py`) because the fixture flattened every opportunity to "Route A — competitive fund." Production reads the real channel/tier from the source reviews, not a heuristic.

## Rebuild

```bash
python3 build_preview.py        # writes /tmp/finance_preview.db
python3 generate_examples.py    # writes the example_*.json
```
