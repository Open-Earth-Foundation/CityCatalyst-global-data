WITH publisher AS (
    SELECT DISTINCT
        publisher_name,
        publisher_url,
        datasource_name,
        dataset_name,
        dataset_url
    FROM raw_data.ct_staging
)
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
SELECT
    (MD5(CONCAT_WS(
        '-', 
        publisher_name, 
        publisher_url
        ))::UUID) AS publisher_id,
    publisher_name,
    publisher_url,
    (MD5(CONCAT_WS(
        '-', 
        datasource_name, 
        dataset_name, 
        dataset_url
        ))::UUID) AS dataset_id,
    datasource_name,
    dataset_name,
    dataset_url
FROM publisher
ON CONFLICT (publisher_id, dataset_id) DO UPDATE SET
    publisher_name = EXCLUDED.publisher_name,
    publisher_url = EXCLUDED.publisher_url,
    datasource_name = EXCLUDED.datasource_name,
    dataset_name = EXCLUDED.dataset_name,
    dataset_url = EXCLUDED.dataset_name;