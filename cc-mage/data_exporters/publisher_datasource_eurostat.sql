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
    MD5('EuroStat-https://ec.europa.eu/eurostat/')::UUID,
    'EuroStat',
    'https://ec.europa.eu/eurostat/',
    MD5('EuroStat-Municipal waste statistics-https://ec.europa.eu/eurostat/statistics-explained/images/b/be/Municipal_waste_statistics_20250210.xlsx')::UUID,
    'EuroStat',
    'Municipal waste statistics',
    'https://ec.europa.eu/eurostat/statistics-explained/images/b/be/Municipal_waste_statistics_20250210.xlsx'
)
ON CONFLICT (publisher_id, dataset_id) DO UPDATE SET
    publisher_name = EXCLUDED.publisher_name,
    publisher_url = EXCLUDED.publisher_url,
    datasource_name = EXCLUDED.datasource_name,
    dataset_name = EXCLUDED.dataset_name,
    dataset_url = EXCLUDED.dataset_url;
