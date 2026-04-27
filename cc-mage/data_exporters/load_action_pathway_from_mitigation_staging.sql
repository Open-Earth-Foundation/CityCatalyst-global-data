-- Replace modelled.action_pathway (+ mitigation_impact) for the three mitigation catalog releases
-- from raw_data.climate_actions_mitigation_staging. release_id UUIDs must match dataset_release inserts.
-- Impacts: emissions_reduction from staging, plus one cobenefit row per JSON array tag (numeric 1, text low).

DELETE FROM modelled.action_pathway
WHERE release_id IN (
    MD5(
        CONCAT_WS(
            '-',
            '{{ c40_datasource_name }}',
            '{{ c40_dataset_name }}',
            '{{ c40_dataset_url }}',
            '{{ mitigation_actions_version_label }}'
        )
    )::UUID,
    MD5(
        CONCAT_WS(
            '-',
            '{{ icare_datasource_name }}',
            '{{ icare_dataset_name }}',
            '{{ icare_dataset_url }}',
            '{{ mitigation_actions_version_label }}'
        )
    )::UUID,
    MD5(
        CONCAT_WS(
            '-',
            '{{ ipcc_datasource_name }}',
            '{{ ipcc_dataset_name }}',
            '{{ ipcc_dataset_url }}',
            '{{ mitigation_actions_version_label }}'
        )
    )::UUID
);

WITH src AS (
    SELECT
        s.src_action_id,
        s.publisher_id,
        NULLIF(TRIM(s.action_type), '') AS action_type,
        NULLIF(TRIM(s.action_role), '') AS action_role,
        NULLIF(TRIM(s.intervention_type), '') AS intervention_type,
        NULLIF(TRIM(s.investment_cost), '') AS investment_cost,
        NULLIF(TRIM(s.implementation_timeline), '') AS implementation_timeline,
        NULLIF(TRIM(s.generation_method), '') AS generation_method,
        NULLIF(TRIM(s.action_name_i18n), '') AS action_name_i18n,
        NULLIF(TRIM(s.description_i18n), '') AS description_i18n,
        NULLIF(TRIM(s.intervention_summary_i18n), '') AS intervention_summary_i18n,
        NULLIF(TRIM(s.outcome_summary_i18n), '') AS outcome_summary_i18n,
        NULLIF(TRIM(s.subsector_number), '') AS subsector_number,
        NULLIF(TRIM(s.gpc_reference_number), '') AS gpc_reference_number,
        NULLIF(TRIM(s.emissions_impact_text), '') AS emissions_impact_text,
        NULLIF(TRIM(s.emissions_impact_numeric), '') AS emissions_impact_numeric,
        NULLIF(TRIM(s.mitigation_source), '') AS mitigation_source
    FROM raw_data.climate_actions_mitigation_staging s
    WHERE NULLIF(TRIM(s.mitigation_source), '') IN ('c40', 'icare', 'ipcc')
),
with_release AS (
    SELECT
        src.*,
        CASE src.mitigation_source
            WHEN 'c40' THEN MD5(
                CONCAT_WS(
                    '-',
                    '{{ c40_datasource_name }}',
                    '{{ c40_dataset_name }}',
                    '{{ c40_dataset_url }}',
                    '{{ mitigation_actions_version_label }}'
                )
            )::UUID
            WHEN 'icare' THEN MD5(
                CONCAT_WS(
                    '-',
                    '{{ icare_datasource_name }}',
                    '{{ icare_dataset_name }}',
                    '{{ icare_dataset_url }}',
                    '{{ mitigation_actions_version_label }}'
                )
            )::UUID
            WHEN 'ipcc' THEN MD5(
                CONCAT_WS(
                    '-',
                    '{{ ipcc_datasource_name }}',
                    '{{ ipcc_dataset_name }}',
                    '{{ ipcc_dataset_url }}',
                    '{{ mitigation_actions_version_label }}'
                )
            )::UUID
        END AS release_id
    FROM src
),
path_rows AS (
    SELECT
        wr.*,
        MD5(CONCAT_WS('-', wr.src_action_id, wr.release_id::TEXT))::UUID AS pathway_id
    FROM with_release wr
    WHERE wr.release_id IS NOT NULL
)
INSERT INTO modelled.action_pathway (
    pathway_id,
    src_action_id,
    publisher_id,
    action_type,
    action_role,
    intervention_type,
    investment_cost,
    implementation_timeline,
    generation_method,
    name_i18n,
    description_i18n,
    intervention_summary_i18n,
    outcome_summary_i18n,
    release_id
)
SELECT
    p.pathway_id,
    p.src_action_id,
    p.publisher_id,
    COALESCE(p.action_type, 'mitigation'),
    p.action_role,
    p.intervention_type,
    p.investment_cost,
    p.implementation_timeline,
    COALESCE(p.generation_method, 'expert_reviewed'),
    CASE
        WHEN p.action_name_i18n IS NULL THEN NULL
        ELSE p.action_name_i18n::JSONB
    END,
    CASE
        WHEN p.description_i18n IS NULL THEN NULL
        ELSE p.description_i18n::JSONB
    END,
    CASE
        WHEN p.intervention_summary_i18n IS NULL THEN NULL
        ELSE p.intervention_summary_i18n::JSONB
    END,
    CASE
        WHEN p.outcome_summary_i18n IS NULL THEN NULL
        ELSE p.outcome_summary_i18n::JSONB
    END,
    p.release_id
FROM path_rows p;

WITH src AS (
    SELECT
        s.src_action_id,
        NULLIF(TRIM(s.subsector_number), '') AS subsector_number,
        NULLIF(TRIM(s.gpc_reference_number), '') AS gpc_reference_number,
        NULLIF(TRIM(s.emissions_impact_text), '') AS emissions_impact_text,
        NULLIF(TRIM(s.emissions_impact_numeric), '') AS emissions_impact_numeric,
        NULLIF(TRIM(s.mitigation_source), '') AS mitigation_source
    FROM raw_data.climate_actions_mitigation_staging s
    WHERE NULLIF(TRIM(s.mitigation_source), '') IN ('c40', 'icare', 'ipcc')
),
with_release AS (
    SELECT
        src.*,
        CASE src.mitigation_source
            WHEN 'c40' THEN MD5(
                CONCAT_WS(
                    '-',
                    '{{ c40_datasource_name }}',
                    '{{ c40_dataset_name }}',
                    '{{ c40_dataset_url }}',
                    '{{ mitigation_actions_version_label }}'
                )
            )::UUID
            WHEN 'icare' THEN MD5(
                CONCAT_WS(
                    '-',
                    '{{ icare_datasource_name }}',
                    '{{ icare_dataset_name }}',
                    '{{ icare_dataset_url }}',
                    '{{ mitigation_actions_version_label }}'
                )
            )::UUID
            WHEN 'ipcc' THEN MD5(
                CONCAT_WS(
                    '-',
                    '{{ ipcc_datasource_name }}',
                    '{{ ipcc_dataset_name }}',
                    '{{ ipcc_dataset_url }}',
                    '{{ mitigation_actions_version_label }}'
                )
            )::UUID
        END AS release_id
    FROM src
),
path_rows AS (
    SELECT
        wr.*,
        MD5(CONCAT_WS('-', wr.src_action_id, wr.release_id::TEXT))::UUID AS pathway_id
    FROM with_release wr
    WHERE wr.release_id IS NOT NULL
)
INSERT INTO modelled.action_pathway_mitigation_impact (
    pathway_impact_id,
    pathway_id,
    subsector_number,
    gpc_reference_number,
    metric_name,
    metric_units,
    metric_value_numeric,
    metric_value_text,
    reporting_year,
    release_id
)
SELECT
    MD5(CONCAT_WS('-', p.pathway_id::TEXT, 'emissions_reduction'))::UUID,
    p.pathway_id,
    p.subsector_number,
    CASE
        WHEN p.gpc_reference_number IS NULL THEN NULL
        ELSE p.gpc_reference_number::JSONB
    END,
    'emissions_reduction',
    'qualitative',
    CASE
        WHEN p.emissions_impact_numeric IS NOT NULL
            AND p.emissions_impact_numeric ~ '^-?[0-9]+(\.[0-9]+)?$'
        THEN p.emissions_impact_numeric::NUMERIC
        ELSE NULL
    END,
    p.emissions_impact_text,
    {{ mitigation_actions_reporting_year }},
    p.release_id
FROM path_rows p
WHERE
    p.emissions_impact_text IS NOT NULL
    OR (
        p.emissions_impact_numeric IS NOT NULL
        AND p.emissions_impact_numeric ~ '^-?[0-9]+(\.[0-9]+)?$'
    )
    OR p.gpc_reference_number IS NOT NULL;

-- One impact row per co-benefit tag from staging ``cobenefits`` JSON array (same numeric/text for all).
WITH src AS (
    SELECT
        s.src_action_id,
        NULLIF(BTRIM(s.cobenefits), '') AS cobenefits,
        NULLIF(TRIM(s.subsector_number), '') AS subsector_number,
        NULLIF(TRIM(s.gpc_reference_number), '') AS gpc_reference_number,
        NULLIF(TRIM(s.mitigation_source), '') AS mitigation_source
    FROM raw_data.climate_actions_mitigation_staging s
    WHERE NULLIF(TRIM(s.mitigation_source), '') IN ('c40', 'icare', 'ipcc')
),
with_release AS (
    SELECT
        src.*,
        CASE src.mitigation_source
            WHEN 'c40' THEN MD5(
                CONCAT_WS(
                    '-',
                    '{{ c40_datasource_name }}',
                    '{{ c40_dataset_name }}',
                    '{{ c40_dataset_url }}',
                    '{{ mitigation_actions_version_label }}'
                )
            )::UUID
            WHEN 'icare' THEN MD5(
                CONCAT_WS(
                    '-',
                    '{{ icare_datasource_name }}',
                    '{{ icare_dataset_name }}',
                    '{{ icare_dataset_url }}',
                    '{{ mitigation_actions_version_label }}'
                )
            )::UUID
            WHEN 'ipcc' THEN MD5(
                CONCAT_WS(
                    '-',
                    '{{ ipcc_datasource_name }}',
                    '{{ ipcc_dataset_name }}',
                    '{{ ipcc_dataset_url }}',
                    '{{ mitigation_actions_version_label }}'
                )
            )::UUID
        END AS release_id
    FROM src
),
path_rows AS (
    SELECT
        wr.*,
        MD5(CONCAT_WS('-', wr.src_action_id, wr.release_id::TEXT))::UUID AS pathway_id
    FROM with_release wr
    WHERE wr.release_id IS NOT NULL
)
INSERT INTO modelled.action_pathway_mitigation_impact (
    pathway_impact_id,
    pathway_id,
    subsector_number,
    gpc_reference_number,
    metric_name,
    metric_units,
    metric_value_numeric,
    metric_value_text,
    reporting_year,
    release_id
)
SELECT
    MD5(CONCAT_WS('-', p.pathway_id::TEXT, 'cobenefit', cb.tag, cb.ord::TEXT))::UUID,
    p.pathway_id,
    p.subsector_number,
    CASE
        WHEN p.gpc_reference_number IS NULL THEN NULL
        ELSE p.gpc_reference_number::jsonb
    END,
    cb.tag,
    'qualitative',
    1::NUMERIC,
    'low',
    {{ mitigation_actions_reporting_year }},
    p.release_id
FROM path_rows p
CROSS JOIN LATERAL jsonb_array_elements_text(BTRIM(p.cobenefits)::jsonb)
    WITH ORDINALITY AS cb (tag, ord)
WHERE p.cobenefits IS NOT NULL
  AND BTRIM(p.cobenefits) <> '[]'
  AND cb.tag <> '';
