-- This script is used to transform the SEEG dataset into a more readable format
-- you need to download the files locally and update the directories
-- This should be executed on DuckDB

CREATE OR REPLACE TABLE seeg_city_emissions AS
SELECT *
FROM read_csv('/Users/<username>/Downloads/Dados por município 11.1*/*/gases.csv', header =True)
WHERE "Setor de emissão" <> 'Setor de emissão'
;

CREATE OR REPLACE TABLE translation_table AS
SELECT *
FROM read_csv('/Users/<username>/Downloads/SEEG to GPC Mapping - DetailedMapping.csv', header = True)
;

CREATE OR REPLACE TABLE seeg_city_emissions_tr AS 
SELECT 		"Emission sector" AS sector,
			"Issuer category" AS category,
			"Issuer sub-category" AS subcategory,
			"Product or system" AS product_or_system,
			'Detailing' AS details,
			'Crop' AS crop,
			"General activity" AS actvity,
			'Biome' AS biome,
			"Issuance/Removal/Bunker" AS emissions_type,
			 replace("Gás", ' (t)', '') AS gas_name,
			 'tonnes' as emissions_units,
			 REGEXP_REPLACE(Cidade, '\s*\(.*?\)','') AS city,
			 REPLACE(REPLACE(REGEXP_EXTRACT(Cidade, '\((.*?)\)'),'(',''),')','') AS region,
			"2015" AS emissions_2015,
			"2016" AS emissions_2016,
			"2017" AS emissions_2017,
			"2018" AS emissions_2018,
			"2019" AS emissions_2019,
			"2020" AS emissions_2020,
			"2021" AS emissions_2021,
			"2022" AS emissions_2022
FROM 		seeg_city_emissions e
LEFT JOIN 	translation_table s
ON 			TRIM(e."Setor de emissão") = TRIM(s."Setor de emissão")
AND 		TRIM(e."Categoria emissora") = TRIM(s."Categoria emissora")
AND  		TRIM(e."Sub-categoria emissora") = TRIM(s."Sub-categoria emissora")
AND 		TRIM(e."Produto ou sistema") = TRIM(s."Produto ou sistema")
AND  		TRIM(e.Detalhamento) = TRIM(s.Detalhamento) 
AND 		TRIM(e.Recorte) = TRIM(s.Recorte)
AND 		TRIM(e."Atividade geral") = TRIM(s."Atividade geral")
AND 		TRIM(e.Bioma) = TRIM(s.Bioma) 
AND 		TRIM(e."Emissão/Remoção/Bunker") = TRIM(s."Emissão/Remoção/Bunker")

-- This will output the table into a directory partitioned by the sector and as a parquet
-- we need to use partitions and parquet format because the dataset is too large otherwise
COPY (
    SELECT *
    FROM seeg_city_emissions_tr
)
TO '/Users/<username>/Documents/seeg_city_emissions/'
WITH (
    FORMAT PARQUET,
    PARTITION_BY (sector)
);
