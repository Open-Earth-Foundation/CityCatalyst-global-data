INSERT INTO modelled.dataset_release (
    release_id,
    publisher_id,
    dataset_id,
    version_label,
    released_at,
    retrieved_at,
    source_url,
    release_notes_url,
    metadata,
    created_at,
    updated_at
)
VALUES (
    MD5('ClimateTRACE-PM2.5-v5_3_0')::uuid,
    MD5('ClimateTRACE-https://climatetrace.org/')::uuid,
    MD5('ClimateTRACE-High Resolution Visualization of PM2.5 Impacts on Surrounding Population-https://downloads.climatetrace.org/latest/country_packages/pm2_5/TCD.zip')::uuid,
    'v5_3_0',
    DATE '2026-01-16',
    NOW(),
    'https://climatetrace.org/',
    'https://github.com/climatetracecoalition/methodology-documents/blob/main/2025/Non%20Greenhouse%20Gases/High%20Resolution%20Visualization%20of%20PM2.5%20Impacts%20on%20Surrounding%20Population-NonGHGSector-112025.pdf',
    '{
        "sector": "Non-GHG",
        "indicator": "PM2.5 impacts",
        "resolution": "high-resolution",
        "source_package": "TCD.zip"
    }'::jsonb,
    NOW(),
    NOW()
);