-- Final cleanup: drop the throwaway raw_data staging tables once modelled is loaded.
-- Recreated next run via replace, so dropping keeps raw_data uncluttered.
DROP TABLE IF EXISTS raw_data.city_finance_profile_staging;
DROP TABLE IF EXISTS raw_data.city_finance_profile_catalog;
