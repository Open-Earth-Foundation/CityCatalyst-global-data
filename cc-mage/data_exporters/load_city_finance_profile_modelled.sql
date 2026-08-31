-- Atomically replace the CITY layer in modelled.city_finance_profile.
-- The explicit retired-source delete is required because v3 changes identity from
-- cl-subdere/cl-subdere-sinim to oef/cl-city-action-fundability. A release-scoped delete of only
-- the new catalog identity would leave the restricted-source rows behind.
-- ids: release_id = MD5(datasource-dataset-version), city_profile_id = MD5(actor_id-release_id).

BEGIN;

DELETE FROM modelled.city_finance_profile
WHERE source_dataset IN (
    'cl-subdere/cl-subdere-sinim',
    'oef/cl-city-action-fundability'
);

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

DO $$
DECLARE
    expected_rows INTEGER;
    inserted_rows INTEGER;
    retired_rows INTEGER;
BEGIN
    SELECT COUNT(DISTINCT actor_id)
    INTO expected_rows
    FROM raw_data.city_finance_profile_staging
    WHERE source_dataset = 'oef/cl-city-action-fundability';

    SELECT COUNT(*)
    INTO inserted_rows
    FROM modelled.city_finance_profile
    WHERE source_dataset = 'oef/cl-city-action-fundability';

    SELECT COUNT(*)
    INTO retired_rows
    FROM modelled.city_finance_profile
    WHERE source_dataset = 'cl-subdere/cl-subdere-sinim';

    IF expected_rows = 0 THEN
        RAISE EXCEPTION 'v3 city-profile staging is empty or has the wrong source identity';
    END IF;
    IF inserted_rows <> expected_rows THEN
        RAISE EXCEPTION 'v3 city-profile row mismatch: expected %, inserted %',
            expected_rows, inserted_rows;
    END IF;
    IF retired_rows <> 0 THEN
        RAISE EXCEPTION 'retired SINIM-backed city-profile rows remain: %', retired_rows;
    END IF;
END $$;

COMMIT;
