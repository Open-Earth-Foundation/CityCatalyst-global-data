-- Final cleanup: drop the pipeline raw_data staging tables once modelled is loaded.
-- Staging is throwaway (recreated next run via replace), so leaving it behind only clutters raw_data.
-- Runs last, downstream of the modelled loads.
DROP TABLE IF EXISTS raw_data.finance_project_staging;
DROP TABLE IF EXISTS raw_data.finance_project_action_staging;
DROP TABLE IF EXISTS raw_data.finance_project_catalog;
