CREATE VIEW finance_action AS
  SELECT b.action_id, b.action_name, b.sector, b.intervention_type,
         b.capital_intensity, b.preparation_complexity,
         k.bench_n_projects, k.bench_duration_median_months, k.bench_duration_n,
         k.bench_cost_median_mmclp, k.bench_cost_n, k.match_confidence,
         b.country_code
  FROM finance_action_base b LEFT JOIN _bench k ON k.action_id = b.action_id;

CREATE TABLE city_finance_profile(
  actor_id TEXT, comuna_cut TEXT, comuna_name TEXT, autonomy REAL, capacity REAL,
  city_archetype TEXT, country_code TEXT);

CREATE TABLE finance_action_base(
  action_id TEXT, action_name TEXT, sector TEXT, intervention_type TEXT,
  capital_intensity REAL, preparation_complexity REAL, country_code TEXT);

CREATE TABLE finance_opportunity(
  source_opportunity_id TEXT, opportunity_name TEXT, funder_name TEXT, funder_level TEXT,
  funder_channel TEXT, instrument TEXT, gpc_sectors TEXT, eligible_actor TEXT,
  city_application TEXT, funding_channel TEXT, access_tier TEXT, open_date TEXT, close_date TEXT,
  status TEXT, status_as_of TEXT, recurrence TEXT, amount_clp REAL, amount_note TEXT,
  climate_relevance TEXT, specificity TEXT, source_url TEXT, country_code TEXT,
  source_dataset TEXT);

CREATE TABLE finance_project(
  source_project_id TEXT, action_id TEXT, project_name TEXT, sector TEXT,
  jurisdiction TEXT, actor_id TEXT, lifecycle_stage TEXT, evaluation_verdict TEXT,
  cost_total REAL, amount_committed REAL, amount_paid REAL, amount_unit TEXT,
  duration_months REAL, beneficiaries_total INTEGER, owner_formulator TEXT,
  match_label TEXT, funding_channel TEXT, funding_sources TEXT,
  country_code TEXT, source_dataset TEXT);

