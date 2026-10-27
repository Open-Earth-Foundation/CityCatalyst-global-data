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
DELETE FROM modelled.action_policy_signals aps
USING release_ctx rc
WHERE aps.release_id = rc.release_id;

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
        TRIM(s.src_action_id) AS src_action_id,
        TRIM(s.location_scope) AS location_scope,
        TRIM(s.location_code) AS location_code,
        TRIM(s.location_name) AS location_name,
        TRIM(s.signal_type) AS signal_type,
        TRIM(s.signal_relation) AS signal_relation,
        TRIM(s.signal_strength) AS signal_strength,
        TRIM(s.explicitness) AS explicitness,
        TRIM(s.document_type) AS document_type,
        TRIM(s.document_name) AS document_name,
        TRIM(s.doc_relevance) AS doc_relevance,
        TRIM(s.signal_summary) AS signal_summary,
        TRIM(s.evidence_text) AS evidence_text,
        NULLIF(TRIM(s.match_type), '') AS match_type,
        NULLIF(TRIM(s.match_reason), '') AS match_reason,
        NULLIF(TRIM(s.page::TEXT), '')::INTEGER AS page
    FROM raw_data.action_policy_signals_staging s
),
deduped AS (
    SELECT DISTINCT ON (
        rc.release_id,
        p.src_action_id,
        p.location_code,
        p.document_name,
        p.page,
        p.signal_type,
        p.signal_relation,
        p.evidence_text
    )
        MD5(
            CONCAT_WS(
                '-',
                rc.release_id::TEXT,
                p.src_action_id,
                p.location_code,
                p.document_name,
                p.page::TEXT,
                p.signal_type,
                p.signal_relation,
                p.evidence_text
            )
        )::UUID AS policy_signal_id,
        p.src_action_id,
        p.location_scope,
        p.location_code,
        p.location_name,
        p.signal_type,
        p.signal_relation,
        p.signal_strength,
        p.explicitness,
        p.document_type,
        p.document_name,
        p.doc_relevance,
        p.signal_summary,
        p.evidence_text,
        p.match_type,
        p.match_reason,
        p.page,
        rc.release_id
    FROM prepared p
    CROSS JOIN release_ctx rc
    ORDER BY
        rc.release_id,
        p.src_action_id,
        p.location_code,
        p.document_name,
        p.page,
        p.signal_type,
        p.signal_relation,
        p.evidence_text
)
INSERT INTO modelled.action_policy_signals (
    policy_signal_id,
    src_action_id,
    location_scope,
    location_code,
    location_name,
    signal_type,
    signal_relation,
    signal_strength,
    explicitness,
    document_type,
    document_name,
    doc_relevance,
    signal_summary,
    evidence_text,
    match_type,
    match_reason,
    page,
    release_id
)
SELECT
    policy_signal_id,
    src_action_id,
    location_scope,
    location_code,
    location_name,
    signal_type,
    signal_relation,
    signal_strength,
    explicitness,
    document_type,
    document_name,
    doc_relevance,
    signal_summary,
    evidence_text,
    match_type,
    match_reason,
    page,
    release_id
FROM deduped
ON CONFLICT (policy_signal_id) DO UPDATE SET
    src_action_id = EXCLUDED.src_action_id,
    location_scope = EXCLUDED.location_scope,
    location_code = EXCLUDED.location_code,
    location_name = EXCLUDED.location_name,
    signal_type = EXCLUDED.signal_type,
    signal_relation = EXCLUDED.signal_relation,
    signal_strength = EXCLUDED.signal_strength,
    explicitness = EXCLUDED.explicitness,
    document_type = EXCLUDED.document_type,
    document_name = EXCLUDED.document_name,
    doc_relevance = EXCLUDED.doc_relevance,
    signal_summary = EXCLUDED.signal_summary,
    evidence_text = EXCLUDED.evidence_text,
    match_type = EXCLUDED.match_type,
    match_reason = EXCLUDED.match_reason,
    page = EXCLUDED.page,
    release_id = EXCLUDED.release_id,
    updated_at = NOW();
