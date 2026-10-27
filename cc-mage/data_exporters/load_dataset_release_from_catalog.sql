INSERT INTO modelled.dataset_release (
    release_id, publisher_id, dataset_id, version_label,
    released_at, retrieved_at, source_url, is_latest
)
SELECT
    c.release_id::UUID, 
    c.publisher_id::UUID, 
    c.dataset_id::UUID, 
    c.version_label,
    CASE WHEN c.released_at ~ '^\d{4}-\d{2}-\d{2}$' THEN c.released_at::DATE END,
    CASE WHEN c.retrieved_at ~ '^\d{4}-\d{2}-\d{2}$' THEN c.retrieved_at::TIMESTAMPTZ END,
    c.source_url,
    true
FROM raw_data.finance_project_catalog c
ON CONFLICT (release_id) DO UPDATE SET
    is_latest = true,
    retrieved_at = EXCLUDED.retrieved_at,
    source_url = EXCLUDED.source_url
