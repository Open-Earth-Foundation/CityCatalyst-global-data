DELETE FROM modelled.finance_project
WHERE release_id IN (SELECT DISTINCT release_id::UUID FROM raw_data.finance_project_catalog);

WITH src AS (
    SELECT
        NULLIF(TRIM(s.source_project_id), '')   AS source_project_id,
        NULLIF(TRIM(s.project_name), '')        AS project_name,
        NULLIF(TRIM(s.project_name_i18n), '')   AS project_name_i18n,
        NULLIF(TRIM(s.sector), '')              AS sector,
        NULLIF(TRIM(s.sector_i18n), '')         AS sector_i18n,
        NULLIF(TRIM(s.jurisdiction), '')        AS jurisdiction,
        NULLIF(TRIM(s.actor_id), '')            AS actor_id,
        NULLIF(TRIM(s.lifecycle_stage), '')     AS lifecycle_stage,
        NULLIF(TRIM(s.evaluation_verdict), '')  AS evaluation_verdict,
        NULLIF(TRIM(s.cost_total), '')          AS cost_total,
        NULLIF(TRIM(s.amount_committed), '')    AS amount_committed,
        NULLIF(TRIM(s.amount_paid), '')         AS amount_paid,
        NULLIF(TRIM(s.amount_unit), '')         AS amount_unit,
        NULLIF(TRIM(s.duration_months), '')     AS duration_months,
        NULLIF(TRIM(s.owner_formulator), '')    AS owner_formulator,
        NULLIF(TRIM(s.funding_channel), '')     AS funding_channel,
        NULLIF(TRIM(s.funding_sources), '')     AS funding_sources,
        NULLIF(TRIM(s.country_code), '')        AS country_code,
        NULLIF(TRIM(s.source_dataset), '')      AS source_dataset
    FROM raw_data.finance_project_staging s
    WHERE NULLIF(TRIM(s.source_project_id), '') IS NOT NULL
),
with_release AS (
    SELECT src.*, c.release_id::UUID AS release_id
    FROM src
    JOIN raw_data.finance_project_catalog c ON c.source_dataset = src.source_dataset
)
INSERT INTO modelled.finance_project (
    project_id, source_project_id, project_name, project_name_i18n,
    sector, sector_i18n, jurisdiction, actor_id, lifecycle_stage, evaluation_verdict,
    cost_total, amount_committed, amount_paid, amount_unit, duration_months, owner_formulator,
    funding_channel, funding_sources, country_code, source_dataset, release_id
)
SELECT
    MD5(CONCAT_WS('-', w.source_project_id, w.release_id::TEXT))::UUID,
    w.source_project_id, w.project_name,
    CASE WHEN w.project_name_i18n ~ '^\s*[\[{]' THEN w.project_name_i18n::JSONB END,
    w.sector,
    CASE WHEN w.sector_i18n ~ '^\s*[\[{]' THEN w.sector_i18n::JSONB END,
    w.jurisdiction, w.actor_id, w.lifecycle_stage, w.evaluation_verdict,
    CASE WHEN w.cost_total       ~ '^-?[0-9]+(\.[0-9]+)?$' THEN w.cost_total::NUMERIC END,
    CASE WHEN w.amount_committed ~ '^-?[0-9]+(\.[0-9]+)?$' THEN w.amount_committed::NUMERIC END,
    CASE WHEN w.amount_paid      ~ '^-?[0-9]+(\.[0-9]+)?$' THEN w.amount_paid::NUMERIC END,
    w.amount_unit,
    CASE WHEN w.duration_months  ~ '^-?[0-9]+(\.[0-9]+)?$' THEN w.duration_months::NUMERIC END,
    w.owner_formulator, w.funding_channel,
    CASE WHEN w.funding_sources ~ '^\s*[\[{]' THEN w.funding_sources::JSONB END,
    w.country_code, w.source_dataset, w.release_id
FROM with_release w
