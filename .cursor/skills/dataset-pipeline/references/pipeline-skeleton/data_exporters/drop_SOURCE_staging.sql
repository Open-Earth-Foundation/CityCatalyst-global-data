-- Template — copy to cc-mage/data_exporters/drop_<SOURCE>_staging.sql.
-- Final cleanup block (downstream of the modelled load): drop the pipeline throwaway
-- raw_data staging table(s). They are recreated by the next run (replace policy), so
-- dropping is safe and keeps raw_data uncluttered. List every staging table the pipeline made.
DROP TABLE IF EXISTS raw_data.<SOURCE>_staging;
