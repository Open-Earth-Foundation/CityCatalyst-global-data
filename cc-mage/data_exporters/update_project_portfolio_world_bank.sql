WITH release_ctx AS (
    SELECT dr.release_id
    FROM modelled.dataset_release dr
    WHERE dr.dataset_id = MD5(CONCAT_WS('-', '{{ datasource_name }}', '{{ dataset_name }}', '{{ dataset_url }}'))::UUID
      AND dr.version_label = '{{ version_label }}'
    LIMIT 1
)
INSERT INTO modelled.project_portfolio (
    project_id,
    source_name,
    source_project_id,
    source_project_url,
    project_name,
    project_description,
    project_status,
    project_type,
    country_code,
    country_name,
    world_region_name,
    approval_at,
    closing_at,
    total_commitment_amount,
    total_project_cost_amount,
    currency_code,
    sector_name,
    theme_name,
    instrument_type,
    borrower_name,
    implementing_agency_name,
    release_id,
    updated_at
)
SELECT DISTINCT
    MD5(CONCAT_WS('-', 'world_bank', COALESCE(wb.id::TEXT, '')))::UUID AS project_id,
    'world_bank' AS source_name,
    wb.id::TEXT AS source_project_id,
    wb.url::TEXT AS source_project_url,
    wb.project_name::TEXT AS project_name,
    NULL::TEXT AS project_description,
    wb._status::TEXT AS project_status,
    wb.lendinginstrtype::TEXT AS project_type,
    NULLIF(
	  (string_to_array(trim(both '{}' from wb.countrycode::text), ','))[1],
	  ''
	) AS country_code,
    NULLIF(
	  (string_to_array(trim(both '{}' from wb.countryshortname::TEXT), ','))[1],
	  ''
	) AS country_name,
    wb.regionname::TEXT AS world_region_name,
    NULLIF(wb.boardapprovaldate::TEXT, '')::TIMESTAMPTZ AS approval_at,
    NULLIF(wb.closingdate::TEXT, '')::TIMESTAMPTZ AS closing_at,
    NULLIF(REPLACE(wb.totalcommamt::TEXT, ',', ''), '')::NUMERIC AS total_commitment_amount,
    NULLIF(REPLACE(wb.lendprojectcost::TEXT, ',', ''), '')::NUMERIC AS total_project_cost_amount,
    NULL::TEXT AS currency_code,
    wb.sector1__name::TEXT AS sector_name,
    NULLIF(TRIM(SPLIT_PART(wb.theme1::TEXT, '!$!', 1)), '')::TEXT AS theme_name,
    wb.lendinginstr::TEXT AS instrument_type,
    wb.borrower::TEXT AS borrower_name,
    wb.impagency::TEXT AS implementing_agency_name,
    rc.release_id,
    NOW() AS updated_at
FROM raw_data.world_bank_projects_staging wb 
JOIN release_ctx rc ON TRUE
WHERE wb.project_name::TEXT IS NOT NULL
AND wb.project_name IS NOT NULL
ON CONFLICT (project_id)
DO UPDATE SET
    source_name = EXCLUDED.source_name,
    source_project_id = EXCLUDED.source_project_id,
    source_project_url = EXCLUDED.source_project_url,
    project_name = EXCLUDED.project_name,
    project_description = EXCLUDED.project_description,
    project_status = EXCLUDED.project_status,
    project_type = EXCLUDED.project_type,
    country_code = EXCLUDED.country_code,
    country_name = EXCLUDED.country_name,
    world_region_name = EXCLUDED.world_region_name,
    approval_at = EXCLUDED.approval_at,
    closing_at = EXCLUDED.closing_at,
    total_commitment_amount = EXCLUDED.total_commitment_amount,
    total_project_cost_amount = EXCLUDED.total_project_cost_amount,
    currency_code = EXCLUDED.currency_code,
    sector_name = EXCLUDED.sector_name,
    theme_name = EXCLUDED.theme_name,
    instrument_type = EXCLUDED.instrument_type,
    borrower_name = EXCLUDED.borrower_name,
    implementing_agency_name = EXCLUDED.implementing_agency_name,
    release_id = EXCLUDED.release_id,
    updated_at = NOW();
