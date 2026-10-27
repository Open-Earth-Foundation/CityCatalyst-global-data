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
DELETE FROM modelled.policy_signals ps
USING release_ctx rc
WHERE ps.release_id = rc.release_id;

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
        s.location_code,
        s.location_name,
        s.location_scope,
        s.signal_type,
        s.signal_relation,
        s.signal_strength,
        s.signal_subject,
        s.gpc_sector,
        s.signal_summary,
        CASE
            WHEN NULLIF(TRIM(s.key_numeric::TEXT), '') IS NULL THEN NULL
            ELSE s.key_numeric::JSONB
        END AS key_numeric,
        CASE
            WHEN NULLIF(TRIM(s.evidence_anchors::TEXT), '') IS NULL THEN NULL
            ELSE s.evidence_anchors::JSONB
        END AS evidence_anchors,
        NULLIF(LPAD(NULLIF(TRIM(s._region_code), ''), 2, '0'), '') AS region_code_2,
        REGEXP_REPLACE(LOWER(COALESCE(s.location_name, '')), '[^a-z0-9]+', '', 'g') AS location_name_norm
    FROM raw_data.cl_ssg_policy_signals_staging s
),
city_match AS (
    SELECT
        cp.locode,
        REGEXP_REPLACE(LOWER(COALESCE(cp.city_name, '')), '[^a-z0-9]+', '', 'g') AS city_name_norm,
        LPAD(NULLIF(TRIM(cp.region_code), ''), 2, '0') AS region_code_2
    FROM modelled.city_polygon cp
    WHERE cp.country_code = 'CL'
),
resolved AS (
    SELECT
        CASE
            WHEN LOWER(COALESCE(st.location_scope, '')) IN ('commune', 'comuna', 'communal', 'city', 'municipal', 'municipality')
                THEN COALESCE(cm_region.locode, cm_name.locode)
            ELSE st.location_code
        END AS location_code,
        st.location_name,
        st.location_scope,
        st.signal_type,
        st.signal_relation,
        st.signal_strength,
        st.signal_subject,
        st.gpc_sector,
        st.signal_summary,
        st.key_numeric,
        st.evidence_anchors
    FROM staged st
    LEFT JOIN city_match cm_region
        ON cm_region.city_name_norm = st.location_name_norm
       AND cm_region.region_code_2 = st.region_code_2
    LEFT JOIN city_match cm_name
        ON cm_name.city_name_norm = st.location_name_norm
),
deduped AS (
    SELECT DISTINCT
        MD5(
            CONCAT_WS(
                '-',
                rc.release_id::TEXT,
                COALESCE(r.location_code, ''),
                COALESCE(r.location_name, ''),
                COALESCE(r.location_scope, ''),
                COALESCE(r.signal_type, ''),
                COALESCE(r.signal_relation, ''),
                COALESCE(r.signal_subject, ''),
                COALESCE(r.gpc_sector, ''),
                COALESCE(r.key_numeric::TEXT, ''),
                COALESCE(r.evidence_anchors::TEXT, '')
            )
        )::UUID AS policy_signal_id,
        r.location_code,
        COALESCE(NULLIF(r.location_name, ''), 'Unknown') AS location_name,
        COALESCE(NULLIF(r.location_scope, ''), 'unspecified') AS location_scope,
        COALESCE(NULLIF(r.signal_type, ''), 'unspecified') AS signal_type,
        COALESCE(NULLIF(r.signal_relation, ''), 'unspecified') AS signal_relation,
        r.signal_strength,
        COALESCE(NULLIF(r.signal_subject, ''), 'unspecified') AS signal_subject,
        r.gpc_sector,
        r.signal_summary,
        r.key_numeric,
        r.evidence_anchors,
        rc.release_id
    FROM resolved r
    CROSS JOIN release_ctx rc
)
INSERT INTO modelled.policy_signals (
    policy_signal_id,
    location_code,
    location_name,
    location_scope,
    signal_type,
    signal_relation,
    signal_strength,
    signal_subject,
    gpc_sector,
    signal_summary,
    key_numeric,
    evidence_anchors,
    release_id
)
SELECT
    policy_signal_id,
    location_code,
    location_name,
    location_scope,
    signal_type,
    signal_relation,
    signal_strength,
    signal_subject,
    gpc_sector,
    signal_summary,
    key_numeric,
    evidence_anchors,
    release_id
FROM deduped
ON CONFLICT (policy_signal_id) DO UPDATE SET
    location_code = EXCLUDED.location_code,
    location_name = EXCLUDED.location_name,
    location_scope = EXCLUDED.location_scope,
    signal_type = EXCLUDED.signal_type,
    signal_relation = EXCLUDED.signal_relation,
    signal_strength = EXCLUDED.signal_strength,
    signal_subject = EXCLUDED.signal_subject,
    gpc_sector = EXCLUDED.gpc_sector,
    signal_summary = EXCLUDED.signal_summary,
    key_numeric = EXCLUDED.key_numeric,
    evidence_anchors = EXCLUDED.evidence_anchors,
    release_id = EXCLUDED.release_id,
    updated_at = NOW();
