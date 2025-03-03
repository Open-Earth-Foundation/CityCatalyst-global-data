DROP TABLE IF EXISTS raw_data.c40_locode_inventories;

CREATE TABLE raw_data.c40_locode_inventories AS
SELECT d.locode, b.iso_code as country_code, a.city, a.emissions_year, a.gpc_reference_number, a.emissions_value, 'c40' as datasource 
FROM raw_data.c40_inventories a
LEFT JOIN raw_data.c40_country_name_lookup b
ON trim(a.country) = trim(b.country)
INNER JOIN modelled.city_polygon d
ON trim(b.iso_code) = substring(d.locode,1,2)
AND trim(lower(case when a.city = 'Montréal' then 'Montreal'
	when a.city = 'New York City' then 'New York'
	else a.city end)) = trim(lower(d.city_name));

-- check there is no duplication 
ALTER TABLE raw_data.c40_locode_inventories
ADD CONSTRAINT unique_locode_emissions_year_gpc_reference
UNIQUE (locode, emissions_year, gpc_reference_number);