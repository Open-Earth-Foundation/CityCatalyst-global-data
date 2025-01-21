WITH seeg_sector_raw_data AS (
SELECT 
    emission_sector,
    case when emission_sector = 'Energy' then general_activity 
        when emission_sector = 'Agriculture' then issuer_subcategory
        when emission_sector = 'Land Use Change and Forestry' then issuer_subcategory
    else null end as activity_name,
    issuer_category,
    issuer_subcategory,
    product_or_system,
    detailing,
    crop,
    general_activity,
    biome,
    emissions_removal,
    s.ipcc_sector,
    g.gpc_mapping,
    gas_name,
    emissions_units,
    city,
    region,
    emissions_2015,
    emissions_2016,
    emissions_2017,
    emissions_2018,
    emissions_2019,
    emissions_2020,
    emissions_2021,
    emissions_2022,
    emissions_2023
FROM 
    {{ df_2 }} e
LEFT JOIN 
    {{ df_3 }} s ON 
    LOWER(TRIM(e.setor_de_emissão)) = LOWER(TRIM(s.setor_de_emissão)) AND 
    LOWER(TRIM(e.categoria_emissora)) = LOWER(TRIM(s.categoria_emissora)) AND 
    LOWER(TRIM(e.subcategoria_emissora)) = LOWER(TRIM(s.subcategoria_emissora)) AND 
    LOWER(TRIM(e.produto_ou_sistema)) = LOWER(TRIM(s.produto_ou_sistema)) AND 
    LOWER(TRIM(e.detalhamento)) = LOWER(TRIM(s.detalhamento)) AND 
    LOWER(TRIM(e.recorte)) = LOWER(TRIM(s.recorte)) AND 
    LOWER(TRIM(e.atividade_geral)) = LOWER(TRIM(s.atividade_geral)) AND 
    LOWER(TRIM(e.bioma)) = LOWER(TRIM(s.bioma)) AND 
    LOWER(TRIM(e.emissão_remoção)) = LOWER(TRIM(s.emissão_remoção))
INNER JOIN 
    {{ df_1 }} g ON 
    g.ipcc_sector = s.ipcc_sector AND 
    g.gpc_mapping NOT LIKE '%+%'
)
SELECT 
    gpc_mapping AS gpc_reference_number,
    gas_name,
    activity_name,
    emissions_units,
    city,
    region,
    SUM(emissions_2015) AS emissions_2015,
    SUM(emissions_2016) AS emissions_2016,
    SUM(emissions_2017) AS emissions_2017,
    SUM(emissions_2018) AS emissions_2018,
    SUM(emissions_2019) AS emissions_2019,
    SUM(emissions_2020) AS emissions_2020,
    SUM(emissions_2021) AS emissions_2021,
    SUM(emissions_2022) AS emissions_2022,
    SUM(emissions_2023) AS emissions_2023
FROM 
    seeg_sector_raw_data
GROUP BY 
    gpc_mapping, 
    gas_name, 
    activity_name,
    emissions_units, 
    city, 
    region