-- Register one publisher_datasource + dataset_release per finance SOURCE dataset,
-- driven by raw_data.finance_source_catalog (built from dataset-review/catalog/index.yaml).
-- Identity is stable slugs only (no dataset_url): dataset_id = MD5(datasource·dataset),
-- release_id = MD5(datasource·dataset·version) — both precomputed in the catalog block.

INSERT INTO modelled.publisher_datasource (
    publisher_id, publisher_name, publisher_url,
    dataset_id, datasource_name, dataset_name, dataset_url
)
SELECT DISTINCT
    c.publisher_id::UUID, c.publisher_name, c.publisher_url,
    c.dataset_id::UUID, c.datasource_name, c.dataset_name, NULLIF(c.dataset_url, '')
FROM raw_data.finance_source_catalog c
ON CONFLICT (publisher_id, dataset_id) DO NOTHING;

-- supersede prior latest releases for these datasets
UPDATE modelled.dataset_release dr
SET is_latest = false
FROM raw_data.finance_source_catalog c
WHERE dr.dataset_id = c.dataset_id::UUID
  AND dr.is_latest = true;

INSERT INTO modelled.dataset_release (
    release_id, publisher_id, dataset_id, version_label,
    released_at, retrieved_at, source_url, is_latest
)
SELECT
    c.release_id::UUID, c.publisher_id::UUID, c.dataset_id::UUID, c.version_label,
    CASE WHEN c.released_at  ~ '^\d{4}-\d{2}-\d{2}$' THEN c.released_at::DATE  END,
    CASE WHEN c.retrieved_at ~ '^\d{4}-\d{2}-\d{2}$' THEN c.retrieved_at::TIMESTAMPTZ END,
    c.source_url,
    true
FROM raw_data.finance_source_catalog c
ON CONFLICT (release_id) DO UPDATE SET
    is_latest    = true,
    retrieved_at = EXCLUDED.retrieved_at,
    source_url   = EXCLUDED.source_url;
