WITH release_ctx AS (
    SELECT MD5(
        CONCAT_WS(
            '-',
            '{{ datasource_name }}',
            '{{ dataset_name }}',
            '{{ dataset_url }}',
            '{{ version_label }}'
        )
    )::UUID AS release_id
),
prepared AS (
    SELECT
        rc.release_id,
        TRIM(s.country_code) AS country_code,
        TRIM(s.action_id) AS src_action_id,
        TRIM(s.global_mitigation_option) AS global_mitigation_option,
        NULLIF(TRIM(s.action_mapping_strength), '') AS action_mapping_strength,
        NULLIF(TRIM(s.option_family), '') AS option_family,
        TRIM(s.feasibility_dimension) AS feasibility_dimension,
        TRIM(s.global_indicator) AS global_indicator,
        TRIM(s.global_verdict_code) AS global_verdict_code,
        NULLIF(TRIM(s.global_verdict_description), '') AS global_verdict_description,
        NULLIF(TRIM(s.city_indicator), '') AS city_indicator,
        NULLIF(TRIM(s.city_indicator_direction), '') AS city_indicator_direction,
        NULLIF(TRIM(s.city_family_scope), '') AS city_family_scope,
        TRIM(s.interpretation) AS interpretation
    FROM raw_data.action_mitigation_feasibility_chain_staging s
    CROSS JOIN release_ctx rc
),
deduped AS (
    SELECT DISTINCT ON (
        p.release_id,
        p.country_code,
        p.src_action_id,
        p.global_mitigation_option,
        p.feasibility_dimension,
        p.global_indicator,
        COALESCE(p.city_indicator, '')
    )
        MD5(
            CONCAT_WS(
                '-',
                p.release_id::TEXT,
                p.country_code,
                p.src_action_id,
                p.global_mitigation_option,
                p.feasibility_dimension,
                p.global_indicator,
                COALESCE(p.city_indicator, '')
            )
        )::UUID AS chain_id,
        p.release_id,
        p.country_code,
        p.src_action_id,
        p.global_mitigation_option,
        p.action_mapping_strength,
        p.option_family,
        p.feasibility_dimension,
        p.global_indicator,
        p.global_verdict_code,
        p.global_verdict_description,
        p.city_indicator,
        p.city_indicator_direction,
        p.city_family_scope,
        p.interpretation
    FROM prepared p
    ORDER BY
        p.release_id,
        p.country_code,
        p.src_action_id,
        p.global_mitigation_option,
        p.feasibility_dimension,
        p.global_indicator,
        COALESCE(p.city_indicator, '')
)
INSERT INTO modelled.action_mitigation_feasibility_chain (
    chain_id,
    release_id,
    country_code,
    src_action_id,
    global_mitigation_option,
    action_mapping_strength,
    option_family,
    feasibility_dimension,
    global_indicator,
    global_verdict_code,
    global_verdict_description,
    city_indicator,
    city_indicator_direction,
    city_family_scope,
    interpretation
)
SELECT
    chain_id,
    release_id,
    country_code,
    src_action_id,
    global_mitigation_option,
    action_mapping_strength,
    option_family,
    feasibility_dimension,
    global_indicator,
    global_verdict_code,
    global_verdict_description,
    city_indicator,
    city_indicator_direction,
    city_family_scope,
    interpretation
FROM deduped
ON CONFLICT (chain_id) DO UPDATE SET
    release_id = EXCLUDED.release_id,
    country_code = EXCLUDED.country_code,
    src_action_id = EXCLUDED.src_action_id,
    global_mitigation_option = EXCLUDED.global_mitigation_option,
    action_mapping_strength = EXCLUDED.action_mapping_strength,
    option_family = EXCLUDED.option_family,
    feasibility_dimension = EXCLUDED.feasibility_dimension,
    global_indicator = EXCLUDED.global_indicator,
    global_verdict_code = EXCLUDED.global_verdict_code,
    global_verdict_description = EXCLUDED.global_verdict_description,
    city_indicator = EXCLUDED.city_indicator,
    city_indicator_direction = EXCLUDED.city_indicator_direction,
    city_family_scope = EXCLUDED.city_family_scope,
    interpretation = EXCLUDED.interpretation,
    updated_at = NOW();
