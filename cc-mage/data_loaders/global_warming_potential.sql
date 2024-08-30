-- Create Table
CREATE TABLE IF NOT EXISTS modelled.global_warming_potential (
    gas_name VARCHAR,
    time_horizon VARCHAR NOT NULL,
    ar2 NUMERIC,
    ar3 NUMERIC,
    ar4 NUMERIC,
    ar5 NUMERIC,
    ar6 NUMERIC
);

-- Insert Data
INSERT INTO modelled.global_warming_potential (gas_name, time_horizon, ar2, ar3, ar4, ar5, ar6) VALUES
('CO2', '100 year', 1, 1, 1, 1, 1),
('CH4', '100 year', 21, 23, 25, 28, NULL),
('N2O', '100 year', 310, 296, 298, 265, 273),
('CH4fossil', '100 year', 21, 23, 25, 28, 29.8),
('CH4nonfossil', '100 year', 21, 23, 25, 28, 27.2);
