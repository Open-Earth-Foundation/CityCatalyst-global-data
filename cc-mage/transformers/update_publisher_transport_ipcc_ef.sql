INSERT INTO modelled.publisher_datasource (
    publisher_id, 
    publisher_name, 
    publisher_url,
    dataset_id,
    datasource_name,
    dataset_name,
    dataset_url
)
SELECT DISTINCT
    publisher_id, 
    publisher_name,
    publisher_url,
    dataset_id,
    datasource_name,
    dataset_name,
    dataset_url
FROM raw_data.ipcc_transport_ef2
ON CONFLICT (publisher_id, dataset_id) 
DO UPDATE SET
    publisher_name = EXCLUDED.publisher_name,
    publisher_url = EXCLUDED.publisher_url,
    datasource_name = EXCLUDED.datasource_name,
    dataset_name = EXCLUDED.dataset_name,
    dataset_url = EXCLUDED.dataset_url;