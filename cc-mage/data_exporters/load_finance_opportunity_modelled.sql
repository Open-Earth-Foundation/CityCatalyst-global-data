-- raw_data.finance_opportunity_staging -> modelled.finance_opportunity
-- Each row inherits its own source-dataset release_id and funder_level from
-- raw_data.finance_source_catalog (built from index.yaml). funder_name is backfilled from
-- the publisher only where the publisher is the funder. Idempotent: release-scoped delete+insert.
-- ids: release_id = MD5(datasource-dataset-version), opportunity_id = MD5(source_opportunity_id-release_id).

DELETE FROM modelled.finance_opportunity
WHERE release_id IN (SELECT DISTINCT release_id::UUID FROM raw_data.finance_source_catalog);

WITH src AS (
    SELECT
        NULLIF(TRIM(s.source_opportunity_id), '')  AS source_opportunity_id,
        NULLIF(TRIM(s.opportunity_name), '')       AS opportunity_name,
        NULLIF(TRIM(s.funder_name), '')            AS funder_name,
        NULL                                        AS funder_level,
        NULLIF(TRIM(s.funder_channel), '')         AS funder_channel,
        NULLIF(TRIM(s.provider), '')               AS provider,
        NULLIF(TRIM(s.instrument), '')             AS instrument,
        NULLIF(TRIM(s.gpc_sectors), '')            AS gpc_sectors,
        NULLIF(TRIM(s.thematic_lines), '')         AS thematic_lines,
        NULLIF(TRIM(s.eligible_actor), '')         AS eligible_actor,
        NULLIF(TRIM(s.eligible_actor_detail), '')  AS eligible_actor_detail,
        NULLIF(TRIM(s.city_application), '')       AS city_application,
        NULLIF(TRIM(s.funding_channel), '')        AS funding_channel,
        NULLIF(TRIM(s.access_tier), '')            AS access_tier,
        NULLIF(TRIM(s.open_date), '')              AS open_date,
        NULLIF(TRIM(s.close_date), '')             AS close_date,
        -- staging column is opportunity_status (Mage mangles the reserved word status to _status)
        NULLIF(TRIM(s.opportunity_status), '')     AS status,
        NULLIF(TRIM(s.status_as_of), '')           AS status_as_of,
        NULLIF(TRIM(s.recurrence), '')             AS recurrence,
        NULLIF(TRIM(s.amount), '')                 AS amount,
        NULL                                        AS amount_currency,
        NULLIF(TRIM(s.amount_note), '')            AS amount_note,
        NULLIF(TRIM(s.climate_relevance), '')      AS climate_relevance,
        NULLIF(TRIM(s.specificity), '')            AS specificity,
        NULLIF(TRIM(s.source_url), '')             AS source_url,
        NULLIF(TRIM(s.legal_basis_url), '')        AS legal_basis_url,
        NULLIF(TRIM(s.data_quality_flags), '')     AS data_quality_flags,
        NULLIF(TRIM(s.source_extras), '')          AS source_extras,
        NULLIF(TRIM(s.notes), '')                  AS notes,
        NULLIF(TRIM(s.country_code), '')           AS country_code,
        NULLIF(TRIM(s.source_dataset), '')         AS source_dataset
    FROM raw_data.finance_opportunity_staging s
    WHERE NULLIF(TRIM(s.source_opportunity_id), '') IS NOT NULL
),
with_release AS (
    -- inherit the source-dataset release_id and publisher fields for the funder backfill
    -- funder_level comes from the staging table (or is NULL if not provided by source)
    SELECT src.*, c.release_id::UUID AS release_id,
           c.publisher_name AS pub_name, c.publisher_is_funder AS pub_is_funder
    FROM src
    JOIN raw_data.finance_source_catalog c ON c.source_dataset = src.source_dataset
)
-- Staging is text. Cast JSONB when the value looks like a JSON array else wrap the scalar,
-- and DATE / NUMERIC only when the text matches the pattern (non-match or null yields NULL).
INSERT INTO modelled.finance_opportunity (
    opportunity_id, source_opportunity_id, opportunity_name, funder_name, funder_level,
    funder_channel, provider, instrument, gpc_sectors, thematic_lines, eligible_actor,
    eligible_actor_detail, city_application, funding_channel, access_tier, open_date, close_date,
    status, status_as_of, recurrence, amount, amount_currency, amount_note, climate_relevance,
    specificity, source_url, legal_basis_url, data_quality_flags, source_extras, notes,
    country_code, source_dataset, release_id
)
SELECT
    MD5(CONCAT_WS('-', w.source_opportunity_id, w.release_id::TEXT))::UUID,
    w.source_opportunity_id, w.opportunity_name,
    COALESCE(w.funder_name, CASE WHEN w.pub_is_funder THEN w.pub_name END), w.funder_level,
    w.funder_channel, w.provider, w.instrument,
    CASE WHEN w.gpc_sectors    ~ '^\s*\[' THEN w.gpc_sectors::JSONB    ELSE to_jsonb(w.gpc_sectors)    END,
    CASE WHEN w.thematic_lines ~ '^\s*\[' THEN w.thematic_lines::JSONB ELSE to_jsonb(w.thematic_lines) END,
    CASE WHEN w.eligible_actor ~ '^\s*\[' THEN w.eligible_actor::JSONB ELSE to_jsonb(w.eligible_actor) END,
    w.eligible_actor_detail,
    CASE WHEN w.city_application ~ '^\s*\[' THEN w.city_application::JSONB ELSE to_jsonb(w.city_application) END,
    w.funding_channel, w.access_tier,
    CASE WHEN w.open_date    ~ '^\d{4}-\d{2}-\d{2}$' THEN w.open_date::DATE    END,
    CASE WHEN w.close_date   ~ '^\d{4}-\d{2}-\d{2}$' THEN w.close_date::DATE   END,
    w.status,
    CASE WHEN w.status_as_of ~ '^\d{4}-\d{2}-\d{2}$' THEN w.status_as_of::DATE END,
    w.recurrence,
    CASE WHEN w.amount ~ '^-?[0-9]+(\.[0-9]+)?$' THEN w.amount::NUMERIC END,
    w.amount_currency, w.amount_note, w.climate_relevance, w.specificity, w.source_url, w.legal_basis_url,
    CASE WHEN w.data_quality_flags IS NULL THEN NULL ELSE w.data_quality_flags::JSONB END,
    CASE WHEN w.source_extras      IS NULL THEN NULL ELSE w.source_extras::JSONB END,
    w.notes, w.country_code, w.source_dataset, w.release_id
FROM with_release w;
