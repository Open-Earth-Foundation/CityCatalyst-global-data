-- C40 high-impact actions (mitigation catalog)
INSERT INTO modelled.publisher_datasource (
    publisher_id,
    publisher_name,
    publisher_url,
    dataset_id,
    datasource_name,
    dataset_slug,
    dataset_name,
    dataset_url
)
VALUES (
    MD5(CONCAT_WS('-', '{{ c40_publisher_name }}', '{{ c40_publisher_url }}'))::UUID,
    '{{ c40_publisher_name }}',
    '{{ c40_publisher_url }}',
    MD5(CONCAT_WS('-', '{{ c40_datasource_name }}', '{{ c40_dataset_name }}', '{{ c40_dataset_url }}'))::UUID,
    '{{ c40_datasource_name }}',
    '{{ c40_datasource_name }}',
    '{{ c40_dataset_name }}',
    '{{ c40_dataset_url }}'
)
ON CONFLICT (publisher_id, dataset_id) DO UPDATE SET
    publisher_name  = EXCLUDED.publisher_name,
    publisher_url   = EXCLUDED.publisher_url,
    datasource_name = EXCLUDED.datasource_name,
    dataset_slug    = EXCLUDED.dataset_slug,
    dataset_name    = EXCLUDED.dataset_name,
    dataset_url     = EXCLUDED.dataset_url;

-- iCARE climate actions
INSERT INTO modelled.publisher_datasource (
    publisher_id,
    publisher_name,
    publisher_url,
    dataset_id,
    datasource_name,
    dataset_slug,
    dataset_name,
    dataset_url
)
VALUES (
    MD5(CONCAT_WS('-', '{{ icare_publisher_name }}', '{{ icare_publisher_url }}'))::UUID,
    '{{ icare_publisher_name }}',
    '{{ icare_publisher_url }}',
    MD5(CONCAT_WS('-', '{{ icare_datasource_name }}', '{{ icare_dataset_name }}', '{{ icare_dataset_url }}'))::UUID,
    '{{ icare_datasource_name }}',
    '{{ icare_datasource_name }}',
    '{{ icare_dataset_name }}',
    '{{ icare_dataset_url }}'
)
ON CONFLICT (publisher_id, dataset_id) DO UPDATE SET
    publisher_name  = EXCLUDED.publisher_name,
    publisher_url   = EXCLUDED.publisher_url,
    datasource_name = EXCLUDED.datasource_name,
    dataset_slug    = EXCLUDED.dataset_slug,
    dataset_name    = EXCLUDED.dataset_name,
    dataset_url     = EXCLUDED.dataset_url;

-- IPCC climate actions
INSERT INTO modelled.publisher_datasource (
    publisher_id,
    publisher_name,
    publisher_url,
    dataset_id,
    datasource_name,
    dataset_slug,
    dataset_name,
    dataset_url
)
VALUES (
    MD5(CONCAT_WS('-', '{{ ipcc_publisher_name }}', '{{ ipcc_publisher_url }}'))::UUID,
    '{{ ipcc_publisher_name }}',
    '{{ ipcc_publisher_url }}',
    MD5(CONCAT_WS('-', '{{ ipcc_datasource_name }}', '{{ ipcc_dataset_name }}', '{{ ipcc_dataset_url }}'))::UUID,
    '{{ ipcc_datasource_name }}',
    '{{ ipcc_datasource_name }}',
    '{{ ipcc_dataset_name }}',
    '{{ ipcc_dataset_url }}'
)
ON CONFLICT (publisher_id, dataset_id) DO UPDATE SET
    publisher_name  = EXCLUDED.publisher_name,
    publisher_url   = EXCLUDED.publisher_url,
    datasource_name = EXCLUDED.datasource_name,
    dataset_slug    = EXCLUDED.dataset_slug,
    dataset_name    = EXCLUDED.dataset_name,
    dataset_url     = EXCLUDED.dataset_url;
