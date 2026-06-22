-- raw_data.city_finance_profile_staging -> modelled.city_finance_profile
-- Each row inherits its source release_id from raw_data.city_finance_profile_catalog (from index.yaml),
-- keyed on source_dataset. Idempotent: release-scoped delete then insert.
-- ids: release_id = MD5(datasource-dataset-version), city_profile_id = MD5(actor_id-release_id).

DELETE FROM modelled.city_finance_profile
WHERE release_id IN (SELECT DISTINCT release_id::UUID FROM raw_data.city_finance_profile_catalog);

WITH src AS (
    SELECT
        NULLIF(TRIM(s.actor_id), '')        AS actor_id,
        NULLIF(TRIM(s.autonomy), '')        AS autonomy,
        NULLIF(TRIM(s.capacity), '')        AS capacity,
        NULLIF(TRIM(s.city_archetype), '')  AS city_archetype,
        NULLIF(TRIM(s.country_code), '')    AS country_code,
        NULLIF(TRIM(s.source_dataset), '')  AS source_dataset
    FROM raw_data.city_finance_profile_staging s
    WHERE NULLIF(TRIM(s.actor_id), '') IS NOT NULL
),
with_release AS (
    SELECT src.*, c.release_id::UUID AS release_id
    FROM src
    JOIN raw_data.city_finance_profile_catalog c ON c.source_dataset = src.source_dataset
)
INSERT INTO modelled.city_finance_profile (
    city_profile_id, actor_id, autonomy, capacity, city_archetype,
    country_code, source_dataset, release_id
)
SELECT
    MD5(CONCAT_WS('-', w.actor_id, w.release_id::TEXT))::UUID,
    w.actor_id,
    CASE WHEN w.autonomy ~ '^-?[0-9]+(\.[0-9]+)?$' THEN w.autonomy::NUMERIC END,
    CASE WHEN w.capacity ~ '^-?[0-9]+(\.[0-9]+)?$' THEN w.capacity::NUMERIC END,
    w.city_archetype, w.country_code, w.source_dataset, w.release_id
FROM with_release w;
