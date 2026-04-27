-- C40: one latest release per dataset (partial unique index on is_latest)
UPDATE modelled.dataset_release
SET is_latest = false
WHERE dataset_id = MD5(CONCAT_WS('-', '{{ c40_datasource_name }}', '{{ c40_dataset_name }}', '{{ c40_dataset_url }}'))::UUID
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
    MD5(CONCAT_WS('-', '{{ c40_datasource_name }}', '{{ c40_dataset_name }}', '{{ c40_dataset_url }}', '{{ mitigation_actions_version_label }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ c40_publisher_name }}', '{{ c40_publisher_url }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ c40_datasource_name }}', '{{ c40_dataset_name }}', '{{ c40_dataset_url }}'))::UUID,
    '{{ mitigation_actions_version_label }}',
    '{{ mitigation_actions_released_at }}'::DATE,
    NOW(),
    '{{ c40_source_url }}',
    true
)
ON CONFLICT (release_id) DO UPDATE SET
    is_latest    = true,
    retrieved_at = NOW(),
    source_url   = EXCLUDED.source_url;

-- iCARE
UPDATE modelled.dataset_release
SET is_latest = false
WHERE dataset_id = MD5(CONCAT_WS('-', '{{ icare_datasource_name }}', '{{ icare_dataset_name }}', '{{ icare_dataset_url }}'))::UUID
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
    MD5(CONCAT_WS('-', '{{ icare_datasource_name }}', '{{ icare_dataset_name }}', '{{ icare_dataset_url }}', '{{ mitigation_actions_version_label }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ icare_publisher_name }}', '{{ icare_publisher_url }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ icare_datasource_name }}', '{{ icare_dataset_name }}', '{{ icare_dataset_url }}'))::UUID,
    '{{ mitigation_actions_version_label }}',
    '{{ mitigation_actions_released_at }}'::DATE,
    NOW(),
    '{{ icare_source_url }}',
    true
)
ON CONFLICT (release_id) DO UPDATE SET
    is_latest    = true,
    retrieved_at = NOW(),
    source_url   = EXCLUDED.source_url;

-- IPCC
UPDATE modelled.dataset_release
SET is_latest = false
WHERE dataset_id = MD5(CONCAT_WS('-', '{{ ipcc_datasource_name }}', '{{ ipcc_dataset_name }}', '{{ ipcc_dataset_url }}'))::UUID
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
    MD5(CONCAT_WS('-', '{{ ipcc_datasource_name }}', '{{ ipcc_dataset_name }}', '{{ ipcc_dataset_url }}', '{{ mitigation_actions_version_label }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ ipcc_publisher_name }}', '{{ ipcc_publisher_url }}'))::UUID,
    MD5(CONCAT_WS('-', '{{ ipcc_datasource_name }}', '{{ ipcc_dataset_name }}', '{{ ipcc_dataset_url }}'))::UUID,
    '{{ mitigation_actions_version_label }}',
    '{{ mitigation_actions_released_at }}'::DATE,
    NOW(),
    '{{ ipcc_source_url }}',
    true
)
ON CONFLICT (release_id) DO UPDATE SET
    is_latest    = true,
    retrieved_at = NOW(),
    source_url   = EXCLUDED.source_url;
