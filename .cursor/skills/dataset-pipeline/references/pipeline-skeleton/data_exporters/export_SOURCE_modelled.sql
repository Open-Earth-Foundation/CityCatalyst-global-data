-- Template — copy to cc-mage/data_exporters/export_<SOURCE>_modelled.sql.
-- raw_data.<SOURCE>_staging -> modelled.<MODELLED_TABLE>.
-- Each row inherits its source-dataset release_id from raw_data.<SOURCE>_source_catalog
-- (produced by the catalog branch: a loader that reads index.yaml from GitHub, then a
-- register-releases SQL block). Copy that branch from the cl_finance_opportunity_to_modelled
-- pipeline (load_finance_source_catalog.py + load_dataset_release_finance_opportunity.sql).
-- Idempotent: release-scoped DELETE + INSERT, so stale rows do not linger.
-- ids: release_id = MD5(datasource-dataset-version) (stable slugs, no dataset_url),
--      <PK> = MD5(<natural_key>-release_id), both precomputed in the catalog block.

-- 1) clear only the releases being loaded (never an unscoped DELETE / TRUNCATE)
DELETE FROM modelled.<MODELLED_TABLE>
WHERE release_id IN (SELECT DISTINCT release_id::UUID FROM raw_data.<SOURCE>_source_catalog);

-- 2) insert fresh, joining the catalog so each row carries its own source release_id
WITH src AS (
    SELECT
        NULLIF(TRIM(s.<natural_key>), '') AS <natural_key>,
        -- NULLIF(TRIM(s.col)) per column, casting JSONB / DATE / NUMERIC with a guard
        NULLIF(TRIM(s.source_dataset), '') AS source_dataset
    FROM raw_data.<SOURCE>_staging s
    WHERE NULLIF(TRIM(s.<natural_key>), '') IS NOT NULL
),
with_release AS (
    SELECT src.*, c.release_id::UUID AS release_id
    FROM src
    JOIN raw_data.<SOURCE>_source_catalog c ON c.source_dataset = src.source_dataset
)
INSERT INTO modelled.<MODELLED_TABLE> (
    <PK>, <natural_key>, /* modelled columns */ release_id
)
SELECT
    MD5(CONCAT_WS('-', w.<natural_key>, w.release_id::TEXT))::UUID,
    w.<natural_key>, /* w.col per column */ w.release_id
FROM with_release w;
