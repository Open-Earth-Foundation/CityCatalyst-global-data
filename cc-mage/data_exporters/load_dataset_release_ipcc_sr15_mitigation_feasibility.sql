UPDATE modelled.dataset_release
SET is_latest = false
WHERE dataset_id = MD5(CONCAT_WS('-', '{{ datasource_name }}', '{{ dataset_name }}', '{{ dataset_url }}'))::UUID
  AND is_latest = true;

INSERT INTO modelled.dataset_release (
    release_id,
    publisher_id,
    dataset_id,
    version_label,
    released_at,
    retrieved_at,
    source_url,
    is_latest
)
VALUES (
    MD5(CONCAT_WS('-', '{{ datasource_name }}', '{{ dataset_name }}', '{{ dataset_url }}', '{{ version_label }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ publisher_name }}', '{{ publisher_url }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ datasource_name }}', '{{ dataset_name }}', '{{ dataset_url }}'))::UUID,
    '{{ version_label }}',
    '{{ released_at }}'::DATE,
    NOW(),
    '{{ source_url }}',
    true
)
ON CONFLICT (release_id) DO UPDATE SET
    is_latest    = true,
    retrieved_at = NOW(),
    source_url   = EXCLUDED.source_url;
