INSERT INTO modelled.dataset_release (
    release_id,
    publisher_id,
    dataset_id,
    version_label,
    released_at,
    retrieved_at,
    source_url
)
VALUES (
    MD5(CONCAT_WS('-', '{{ datasource_name }}', '{{ dataset_name }}', '{{ dataset_url }}', '{{ version_label }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ publisher_name }}', '{{ publisher_url }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ datasource_name }}', '{{ dataset_name }}', '{{ dataset_url }}'))::UUID,
    '{{ version_label }}',
    '{{ released_at }}'::DATE,
    NOW(),
    '{{ source_url }}'
)
ON CONFLICT (release_id) DO UPDATE SET
    retrieved_at = NOW(),
    source_url   = EXCLUDED.source_url;
