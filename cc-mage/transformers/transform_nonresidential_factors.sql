WITH ibge_nonres_scaling AS (
SELECT *
FROM {{ df_1 }}
UNION
SELECT *
FROM {{ df_2 }}
UNION
SELECT *
FROM {{ df_3 }}
),
ibge_nonres_scaling_pivot AS (
SELECT 
    city_name,
    region_code,
    scaling_factor_description,
    units,
    factor_year,
    factor_value::numeric/ 100 as factor_value
FROM (
    SELECT 
        STRING_SPLIT(localidade_nome, '-')[1] AS city_name,
        STRING_SPLIT(localidade_nome, '-')[2] AS region_code,
        CASE 
            WHEN _variable = 'Participação do valor adicionado bruto a preços correntes total no valor adicionado bruto a preços correntes total da unidade da federação' THEN 'city percentage gross value added to state'
            WHEN _variable = 'Participação do valor adicionado bruto a preços correntes da agropecuária no valor adicionado bruto a preços correntes da agropecuária da unidade da federação' THEN 'city percentage gross value added by agriculture to state'
            WHEN _variable = 'Participação do valor adicionado bruto a preços correntes da indústria no valor adicionado bruto a preços correntes da indústria da unidade da federação' THEN 'city percentage gross value added by industrial to state'
            ELSE NULL 
        END AS scaling_factor_description,
        units,
        serie_2015,
        serie_2016,
        serie_2017,
        serie_2018,
        serie_2019,
        serie_2020,
        serie_2021
    FROM ibge_nonres_scaling
) AS source_data
UNPIVOT (
    factor_value FOR factor_year IN (
        serie_2015 AS '2015',
        serie_2016 AS '2016',
        serie_2017 AS '2017',
        serie_2018 AS '2018',
        serie_2019 AS '2019',
        serie_2020 AS '2020',
        serie_2021 AS '2021'
    )
) AS unpivoted_data
),
ibge_res_scale AS (
SELECT STRING_SPLIT(a.localidade_nome, '-')[1] AS city_name,
        STRING_SPLIT(a.localidade_nome, '-')[2] AS region_code,
        'city percentage of residential population state' AS scaling_factor_description,
        '%' as units,
        2022 as factor_year,
        a.serie_2022::numeric/ b.serie_2022::numeric as factor_value
        -- a.serie_2022 as city_respop,
        -- b.serie_2022 as region_respop   
FROM {{ df_4 }} a 
INNER JOIN {{ df_5 }} b 
ON TRIM(STRING_SPLIT(a.localidade_nome, '-')[2]) = (
    CASE 
    WHEN b.localidade_nome = 'Rondônia' THEN 'RO'
    WHEN b.localidade_nome = 'Acre' THEN 'AC'
    WHEN b.localidade_nome = 'Amazonas' THEN 'AM'
    WHEN b.localidade_nome = 'Roraima' THEN 'RR'
    WHEN b.localidade_nome = 'Pará' THEN 'PA'
    WHEN b.localidade_nome = 'Amapá' THEN 'AP'
    WHEN b.localidade_nome = 'Tocantins' THEN 'TO'
    WHEN b.localidade_nome = 'Maranhão' THEN 'MA'
    WHEN b.localidade_nome = 'Piauí' THEN 'PI'
    WHEN b.localidade_nome = 'Ceará' THEN 'CE'
    WHEN b.localidade_nome = 'Rio Grande do Norte' THEN 'RN'
    WHEN b.localidade_nome = 'Paraíba' THEN 'PB'
    WHEN b.localidade_nome = 'Pernambuco' THEN 'PE'
    WHEN b.localidade_nome = 'Alagoas' THEN 'AL'
    WHEN b.localidade_nome = 'Sergipe' THEN 'SE'
    WHEN b.localidade_nome = 'Bahia' THEN 'BA'
    WHEN b.localidade_nome = 'Minas Gerais' THEN 'MG'
    WHEN b.localidade_nome = 'Espírito Santo' THEN 'ES'
    WHEN b.localidade_nome = 'Rio de Janeiro' THEN 'RJ'
    WHEN b.localidade_nome = 'São Paulo' THEN 'SP'
    WHEN b.localidade_nome = 'Paraná' THEN 'PR'
    WHEN b.localidade_nome = 'Santa Catarina' THEN 'SC'
    WHEN b.localidade_nome = 'Rio Grande do Sul' THEN 'RS'
    WHEN b.localidade_nome = 'Mato Grosso do Sul' THEN 'MS'
    WHEN b.localidade_nome = 'Mato Grosso' THEN 'MT'
    WHEN b.localidade_nome = 'Goiás' THEN 'GO'
    WHEN b.localidade_nome = 'Distrito Federal' THEN 'DF'
    ELSE NULL
END 
)
)
SELECT *
FROM ibge_res_scale
UNION
SELECT *
FROM ibge_nonres_scaling_pivot