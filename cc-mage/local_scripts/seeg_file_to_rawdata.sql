-- This script is used to transform the SEEG dataset into a more readable format
-- you need to download the files locally and update the directories
-- This should be executed on DuckDB

CREATE OR REPLACE TABLE seeg_city_emissions AS
SELECT 		"Setor de emissão" AS setor_de_emissão,
			"Categoria emissora" AS categoria_emissora,
			"Sub-categoria emissora" AS subcategoria_emissora,
			"Produto ou sistema" AS produto_ou_sistema,
			Detalhamento AS detalhamento,
			Recorte AS recorte,
			"Atividade geral" AS atividade_geral,
			Bioma AS bioma,
			"Emissão/Remoção/Bunker" AS emissão_remoção,
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
FROM read_csv('/Users/amandaeames/Downloads/Dados por município 11.1*/*/gases.csv', header =True)
WHERE "Setor de emissão" <> 'Setor de emissão'
;

-- This will output the table into a directory partitioned by the sector and as a parquet
-- we need to use partitions and parquet format because the dataset is too large otherwise
COPY (
    SELECT *
    FROM seeg_city_emissions
)
TO '/Users/<username>/Documents/seeg_city_emissions/'
WITH (
    FORMAT PARQUET,
    PARTITION_BY (sector)
);
