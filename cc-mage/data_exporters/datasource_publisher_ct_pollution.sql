INSERT INTO modelled.publisher_datasource 
(
    publisher_id, 
    publisher_name, 
    publisher_url, 
    dataset_id, 
    datasource_name, 
    dataset_name, 
    dataset_url
)
VALUES (
    MD5('ClimateTRACE-https://climatetrace.org/')::UUID,
    'ClimateTRACE',
    'https://climatetrace.org/',
    MD5('ClimateTRACE-High Resolution Visualization of PM2.5 Impacts on Surrounding Population-https://downloads.climatetrace.org/latest/country_packages/pm2_5/TCD.zip')::UUID,
    'ClimateTRACE',
    'High Resolution Visualization of PM2.5 Impacts on Surrounding Population',
    'https://downloads.climatetrace.org/latest/country_packages/pm2_5/TCD.zip'
)
ON CONFLICT (publisher_id, dataset_id) DO UPDATE SET
    publisher_name = EXCLUDED.publisher_name,
    publisher_url = EXCLUDED.publisher_url,
    datasource_name = EXCLUDED.datasource_name,
    dataset_name = EXCLUDED.dataset_name,
    dataset_url = EXCLUDED.dataset_url;
