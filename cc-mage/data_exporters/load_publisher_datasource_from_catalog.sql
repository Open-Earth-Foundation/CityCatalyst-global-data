INSERT INTO modelled.publisher_datasource (
    publisher_id, publisher_name, publisher_url,
    dataset_id, datasource_name, dataset_name, dataset_url
)
SELECT DISTINCT
    c.publisher_id::UUID, 
    c.publisher_name, 
    c.publisher_url,
    c.dataset_id::UUID, 
    c.datasource_name, 
    c.dataset_name,
    COALESCE(NULLIF(c.dataset_url, ''), c.source_url)
FROM raw_data.finance_project_catalog c
ON CONFLICT (publisher_id, dataset_id) DO UPDATE SET
    datasource_name = EXCLUDED.datasource_name,
    dataset_name = EXCLUDED.dataset_name,
    dataset_url = EXCLUDED.dataset_url
