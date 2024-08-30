WITH city_comparisons AS (
  SELECT * FROM (
    VALUES
    ('Arês', 'RN', 'Arez', 'RN'),
    ('Açu', 'RN', 'Assu', 'RN'),
    ('Bocaiúva', 'MG', 'Bocaiuva', 'MG'),
    ('Crateús', 'CE', 'osm', 'CE'),
    ('Gracho Cardoso', 'SE', 'Graccho Cardoso', 'SE'),
    ('Guatambú', 'SC', 'Guatambu', 'SC'),
    ('Itapecuru Mirim', 'MA', 'Itapecuru-Mirim', 'MA'),
    ('Januário Cicco', 'RN', 'Boa Saúde', 'RN'),
    ('Lagoa dos Patos', 'RS', NULL, 'RS'),
    ('Lagoa Mirim', 'RS', NULL, 'RS'),
    ('Lajedo do Tabocal', 'BA', 'Lagedo do Tabocal', 'BA'),
    ('Lindóia', 'SP', 'Lindoia', 'SP'),
    ('Luís Antônio', 'SP', 'Luiz Antônio', 'SP'),
    ('Major Isidoro', 'AL', 'Major Izidoro', 'AL'),
    ('Maturéia', 'PB', 'Matureia', 'PB'),
    ('Mauriti', 'CE', 'osm', 'CE'),
    ('Olho d''Água do Borges', 'RN', 'Olho-d''Água do Borges', 'RN'), 
    ('Paulicéia', 'SP', 'Pauliceia', 'SP'),
    ('Pompéia', 'SP', 'Pompeia', 'SP'),
    ('Rio do Prado', 'MG', 'osm', 'MG'),
    ('Santa Teresinha', 'PB', 'Santa Terezinha', 'PB'),
    ('Santa Terezinha', 'BA', 'Santa Teresinha', 'BA'),
    ('Santo Antônio do Leverger', 'MT', 'Santo Antônio de Leverger', 'MT'),
    ('São Caitano', 'PE', 'São Caetano', 'PE'),
    ('São João del Rei', 'MG', 'São João del-Rei', 'MG'),
    ('São Luis do Piauí', 'PI', 'São Luís do Piauí', 'PI')
  ) AS t(seeg_city, seeg_region, overture_city, overture_region)
)
SELECT 		DISTINCT COALESCE(cc.seeg_city, d.primary_name) as city,
			d.region,
			lo.locode,
            d.osm_id,
			d.geometry
FROM 		{{ df_1 }} d
LEFT JOIN 	city_comparisons cc 
ON 			d.primary_name = cc.overture_city
AND 		d.region = cc.overture_region
INNER JOIN 	{{ df_2 }} lo 
ON 			REPLACE(LOWER(TRIM(CASE WHEN COALESCE(cc.seeg_city, d.primary_name) = 'Santa Terezinha' AND REPLACE(d.region, 'BR-', '') = 'BA' THEN 'Santa Teresinha'
			WHEN COALESCE(cc.seeg_city, d.primary_name) = 'Amparo do São Francisco' AND REPLACE(d.region, 'BR-', '') = 'SE' THEN 'Amparo de São Francisco'
			WHEN COALESCE(cc.seeg_city, d.primary_name) = 'Atílio Vivácqua' AND REPLACE(d.region, 'BR-', '')= 'ES' THEN 'Atilio Vivacqua' ELSE COALESCE(cc.seeg_city, d.primary_name) END )), '-', ' ') = replace(lower(trim(lo._name)), '-', ' ') 
AND 		d.region = lo.SubDiv
;