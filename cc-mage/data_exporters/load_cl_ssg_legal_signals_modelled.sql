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
)
DELETE FROM modelled.action_legal_assessement ala
USING release_ctx rc
WHERE ala.release_id = rc.release_id;

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
staged AS (
    SELECT
        MD5(
            CONCAT_WS(
                '-',
                rc.release_id::TEXT,
                TRIM(s.country_code),
                TRIM(s.src_action_id)
            )
        )::UUID AS legal_analysis_id,
        TRIM(s.src_action_id) AS src_action_id,
        TRIM(s.country_code) AS country_code,
        NULLIF(TRIM(s.gpc_sector), '') AS gpc_sector,
        NULLIF(TRIM(s.verdict_category), '') AS verdict_category,
        NULLIF(TRIM(s.verdict_score), '')::NUMERIC AS verdict_score,
        NULLIF(TRIM(s.ownership_category), '') AS ownership_category,
        NULLIF(TRIM(s.ownership_score), '')::NUMERIC AS ownership_score,
        NULLIF(TRIM(s.ownership_weight), '')::NUMERIC AS ownership_weight,
        COALESCE(
            NULLIF(TRIM(s.ownership_description_en), ''),
            NULLIF(TRIM(s.ownership_description_es), '')
        ) AS ownership_description,
        NULLIF(TRIM(s.restrictions_category), '') AS restrictions_category,
        NULLIF(TRIM(s.restrictions_score), '')::NUMERIC AS restrictions_score,
        NULLIF(TRIM(s.restrictions_weight), '')::NUMERIC AS restrictions_weight,
        COALESCE(
            NULLIF(TRIM(s.restrictions_description_en), ''),
            NULLIF(TRIM(s.restrictions_description_es), '')
        ) AS restrictions_description,
        COALESCE(
            NULLIF(TRIM(s.legal_justification_en), ''),
            NULLIF(TRIM(s.legal_justification_es), '')
        ) AS legal_justification,
        CASE
            WHEN NULLIF(TRIM(s.analysis_date), '') IS NULL THEN NULL
            ELSE TRIM(s.analysis_date)::DATE
        END AS analysis_date,
        TRIM(s.generation_method) AS generation_method,
        (
            SELECT jsonb_agg(elem ORDER BY ord)
            FROM (
                SELECT 1 AS ord, NULLIF(TRIM(s.legal_reference_1), '') AS elem
                UNION ALL SELECT 2, NULLIF(TRIM(s.legal_reference_2), '')
                UNION ALL SELECT 3, NULLIF(TRIM(s.legal_reference_3), '')
                UNION ALL SELECT 4, NULLIF(TRIM(s.legal_reference_4), '')
                UNION ALL SELECT 5, NULLIF(TRIM(s.legal_reference_5), '')
                UNION ALL SELECT 6, NULLIF(TRIM(s.legal_reference_6), '')
            ) r
            WHERE r.elem IS NOT NULL
        ) AS legal_references,
        CASE
            WHEN NULLIF(TRIM(s.ownership_description_en), '') IS NULL
                 AND NULLIF(TRIM(s.ownership_description_es), '') IS NULL
            THEN NULL
            ELSE jsonb_strip_nulls(
                jsonb_build_object(
                    'en', NULLIF(TRIM(s.ownership_description_en), ''),
                    'es', NULLIF(TRIM(s.ownership_description_es), '')
                )
            )
        END AS ownership_description_i18n,
        CASE
            WHEN NULLIF(TRIM(s.restrictions_description_en), '') IS NULL
                 AND NULLIF(TRIM(s.restrictions_description_es), '') IS NULL
            THEN NULL
            ELSE jsonb_strip_nulls(
                jsonb_build_object(
                    'en', NULLIF(TRIM(s.restrictions_description_en), ''),
                    'es', NULLIF(TRIM(s.restrictions_description_es), '')
                )
            )
        END AS restrictions_description_i18n,
        CASE
            WHEN NULLIF(TRIM(s.legal_justification_en), '') IS NULL
                 AND NULLIF(TRIM(s.legal_justification_es), '') IS NULL
            THEN NULL
            ELSE jsonb_strip_nulls(
                jsonb_build_object(
                    'en', NULLIF(TRIM(s.legal_justification_en), ''),
                    'es', NULLIF(TRIM(s.legal_justification_es), '')
                )
            )
        END AS legal_justification_i18n,
        rc.release_id
    FROM raw_data.cl_ssg_legal_signals_staging s
    CROSS JOIN release_ctx rc
    -- Modelled only: omit staging rows with no verdict (placeholders / not analysed).
    WHERE NULLIF(TRIM(s.verdict_category), '') IS NOT NULL
)
INSERT INTO modelled.action_legal_assessement (
    legal_analysis_id,
    src_action_id,
    country_code,
    gpc_sector,
    verdict_category,
    verdict_score,
    ownership_category,
    ownership_score,
    ownership_weight,
    ownership_description,
    restrictions_category,
    restrictions_score,
    restrictions_weight,
    restrictions_description,
    legal_justification,
    analysis_date,
    generation_method,
    legal_references,
    release_id,
    ownership_description_i18n,
    restrictions_description_i18n,
    legal_justification_i18n
)
SELECT
    legal_analysis_id,
    src_action_id,
    country_code,
    gpc_sector,
    verdict_category,
    verdict_score,
    ownership_category,
    ownership_score,
    ownership_weight,
    ownership_description,
    restrictions_category,
    restrictions_score,
    restrictions_weight,
    restrictions_description,
    legal_justification,
    analysis_date,
    generation_method,
    legal_references,
    release_id,
    ownership_description_i18n,
    restrictions_description_i18n,
    legal_justification_i18n
FROM staged
ON CONFLICT (legal_analysis_id) DO UPDATE SET
    src_action_id = EXCLUDED.src_action_id,
    country_code = EXCLUDED.country_code,
    gpc_sector = EXCLUDED.gpc_sector,
    verdict_category = EXCLUDED.verdict_category,
    verdict_score = EXCLUDED.verdict_score,
    ownership_category = EXCLUDED.ownership_category,
    ownership_score = EXCLUDED.ownership_score,
    ownership_weight = EXCLUDED.ownership_weight,
    ownership_description = EXCLUDED.ownership_description,
    restrictions_category = EXCLUDED.restrictions_category,
    restrictions_score = EXCLUDED.restrictions_score,
    restrictions_weight = EXCLUDED.restrictions_weight,
    restrictions_description = EXCLUDED.restrictions_description,
    legal_justification = EXCLUDED.legal_justification,
    analysis_date = EXCLUDED.analysis_date,
    generation_method = EXCLUDED.generation_method,
    legal_references = EXCLUDED.legal_references,
    release_id = EXCLUDED.release_id,
    ownership_description_i18n = EXCLUDED.ownership_description_i18n,
    restrictions_description_i18n = EXCLUDED.restrictions_description_i18n,
    legal_justification_i18n = EXCLUDED.legal_justification_i18n,
    updated_at = NOW();
