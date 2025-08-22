CREATE TABLE IF NOT EXISTS modelled.publisher_datasource (
  publisher_id uuid,
  publisher_name VARCHAR NOT NULL,
  publisher_url VARCHAR NOT NULL,
  dataset_id uuid,
  datasource_name VARCHAR NOT NULL,
  dataset_name VARCHAR NOT NULL,
  dataset_url VARCHAR NOT NULL,
  PRIMARY KEY (publisher_id, dataset_id)
)
