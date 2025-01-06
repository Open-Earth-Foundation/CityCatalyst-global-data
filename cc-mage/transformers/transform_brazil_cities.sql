WITH region_mapping AS (
    SELECT 'Acre' AS region_name, 'AC' AS region_code UNION ALL
    SELECT 'Alagoas', 'AL' UNION ALL
    SELECT 'Amapá', 'AP' UNION ALL
    SELECT 'Amazonas', 'AM' UNION ALL
    SELECT 'Bahia', 'BA' UNION ALL
    SELECT 'Ceará', 'CE' UNION ALL
    SELECT 'Distrito Federal', 'DF' UNION ALL
    SELECT 'Espírito Santo', 'ES' UNION ALL
    SELECT 'Goiás', 'GO' UNION ALL
    SELECT 'Maranhão', 'MA' UNION ALL
    SELECT 'Mato Grosso', 'MT' UNION ALL
    SELECT 'Mato Grosso do Sul', 'MS' UNION ALL
    SELECT 'Minas Gerais', 'MG' UNION ALL
    SELECT 'Paraná', 'PR' UNION ALL
    SELECT 'Paraíba', 'PB' UNION ALL
    SELECT 'Pará', 'PA' UNION ALL
    SELECT 'Pernambuco', 'PE' UNION ALL
    SELECT 'Piauí', 'PI' UNION ALL
    SELECT 'Rio de Janeiro', 'RJ' UNION ALL
    SELECT 'Rio Grande do Norte', 'RN' UNION ALL
    SELECT 'Rio Grande do Sul', 'RS' UNION ALL
    SELECT 'Rondônia', 'RO' UNION ALL
    SELECT 'Roraima', 'RR' UNION ALL
    SELECT 'Santa Catarina', 'SC' UNION ALL
    SELECT 'Sergipe', 'SE' UNION ALL
    SELECT 'São Paulo', 'SP' UNION ALL
    SELECT 'Tocantins', 'TO'
),
locode_data AS (
    SELECT 
        a.LOCODE AS locode,
        a._Name AS city_name,
        a.SubDiv AS region_code
    FROM {{ df_2 }} a
),
city_comparison AS (
  SELECT * FROM (
    VALUES
    ('Graccho Cardoso', 'SE', 'Gracho Cardoso', 'SE'),
    ('Amparo do São Francisco', 'SE', 'Amparo de São Francisco', 'SE'),
    ('Barão do Monte Alto', 'MG', 'Barão de Monte Alto', 'MG'),
    ('Santo Antônio de Leverger', 'MT', 'Santo Antônio do Leverger', 'MT'),
    ('Atílio Vivácqua', 'ES', 'Atilio Vivacqua', 'ES'),
    ('Santa Terezinha', 'BA', 'Santa Teresinha', 'BA')
  ) AS t(src_city_name, src_region_code, locode_city_name, locode_region)
)
SELECT 	ld.locode,		
		bb.city_name,
		rm.region_code,
        bb.geom
		--ST_GeomFromHEXWKB(bb.geom) as geometry		
FROM {{ df_1 }} bb
LEFT JOIN region_mapping rm 
ON bb.region_name = rm.region_name
LEFT JOIN city_comparison cc 
ON bb.city_name = cc.src_city_name
AND rm.region_code = cc.src_region_code
LEFT JOIN locode_data ld 
ON REPLACE(LOWER(COALESCE(cc.locode_city_name,bb.city_name)), '-', ' ') = REPLACE(LOWER(ld.city_name), '-', ' ')
AND rm.region_code = ld.region_code
WHERE ld.locode IS NOT NULL;  