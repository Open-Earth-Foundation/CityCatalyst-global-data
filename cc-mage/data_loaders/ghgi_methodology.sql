CREATE TABLE IF NOT EXISTS modelled.ghgi_methodology (
  method_id uuid,
  methodology_name VARCHAR NOT NULL,
  methodology_description VARCHAR NOT NULL,
  gpc_reference_number VARCHAR NOT NULL,
  PRIMARY KEY (method_id)
)
