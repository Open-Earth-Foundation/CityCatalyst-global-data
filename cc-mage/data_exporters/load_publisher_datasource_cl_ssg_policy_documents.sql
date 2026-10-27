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
    MD5(CONCAT_WS('-', '{{ publisher_name }}', '{{ publisher_url }}'))::UUID,
    '{{ publisher_name }}',
    '{{ publisher_url }}',
    MD5(CONCAT_WS('-', '{{ datasource_name }}', '{{ dataset_name }}', '{{ dataset_url }}'))::UUID,
    '{{ datasource_name }}',
    '{{ datasource_name }}',
    '{{ dataset_name }}',
    '{{ dataset_url }}'
)
ON CONFLICT (publisher_id, dataset_id) DO UPDATE SET
    publisher_name  = EXCLUDED.publisher_name,
    publisher_url   = EXCLUDED.publisher_url,
    datasource_name = EXCLUDED.datasource_name,
    dataset_slug    = EXCLUDED.dataset_slug,
    dataset_name    = EXCLUDED.dataset_name,
    dataset_url     = EXCLUDED.dataset_url;
