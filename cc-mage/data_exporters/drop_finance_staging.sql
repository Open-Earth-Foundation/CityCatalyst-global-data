-- Final cleanup: drop the pipeline raw_data staging tables once modelled is loaded.
-- Staging is throwaway (recreated on the next run via replace), so leaving it
-- behind only clutters raw_data. Runs last, downstream of load_finance_opportunity_modelled.
DROP TABLE IF EXISTS raw_data.finance_opportunity_staging;
DROP TABLE IF EXISTS raw_data.finance_source_catalog;
