-- Register one publisher_datasource + dataset_release for the city_finance_profile SOURCE dataset
-- (oef/cl-city-action-fundability v3), driven by raw_data.city_finance_profile_catalog.
-- Identity is stable slugs only (dataset_url is descriptive, not part of either ID):
-- dataset_id = MD5(datasource-dataset), release_id = MD5(datasource-dataset-version).

INSERT INTO modelled.publisher_datasource (
    publisher_id, publisher_name, publisher_url,
    dataset_id, datasource_name, dataset_name, dataset_url
)
SELECT DISTINCT
    c.publisher_id::UUID, c.publisher_name, c.publisher_url,
    c.dataset_id::UUID, c.datasource_name, c.dataset_name,
    COALESCE(NULLIF(c.dataset_url, ''), c.source_url)
FROM raw_data.city_finance_profile_catalog c
ON CONFLICT (publisher_id, dataset_id) DO UPDATE SET
    datasource_name = EXCLUDED.datasource_name,
    dataset_name     = EXCLUDED.dataset_name,
    dataset_url      = EXCLUDED.dataset_url;

UPDATE modelled.dataset_release dr
SET is_latest = false
FROM raw_data.city_finance_profile_catalog c
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
FROM raw_data.city_finance_profile_catalog c
ON CONFLICT (release_id) DO UPDATE SET
    is_latest    = true,
    retrieved_at = EXCLUDED.retrieved_at,
    source_url   = EXCLUDED.source_url;
