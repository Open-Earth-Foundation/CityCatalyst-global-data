CREATE OR REPLACE TABLE target_indicator AS
WITH RECURSIVE hierarchy AS (
    -- Start the hierarchy with root nodes (where indicator_id_master is NULL)
    SELECT 
        id,
        indicator_id_master,
        1 AS level,
        ARRAY[id] AS path
    FROM 
        {{ df_1 }} 
    WHERE 
        indicator_id_master IS NULL
    UNION ALL
    -- Recursively join child nodes to their parents based on indicator_id_master
    SELECT 
        t.id,
        t.indicator_id_master,
        h.level + 1 AS level,
        array_append(h.path, t.id) AS path
    FROM 
        {{ df_1 }}  t
    JOIN 
        hierarchy h ON t.indicator_id_master = h.id
),
flat_hierarchy AS (
    -- Simplified flat hierarchy extraction
    SELECT 
        id AS leaf_id,
        path,
        level
    FROM 
        hierarchy
),
hierarchy_level AS (
    -- Join back to indicators to get names and organize hierarchy levels
    SELECT 
        c.level_1_id,
        i._name AS level_1_name,
        c.level_2_id, 
        i2._name AS level_2_name,
        c.level_3_id, 
        i3._name AS level_3_name,
        c.level_4_id, 
        i4._name AS level_4_name,
        c.level_5_id, 
        i5._name AS level_5_name,
        c.level_6_id, 
        i6._name AS level_6_name,
        c.level,
        c.leaf_id
    FROM (
        SELECT 
            path[1] AS level_1_id,
            path[2] AS level_2_id,
            path[3] AS level_3_id,
            path[4] AS level_4_id,
            path[5] AS level_5_id,
            path[6] AS level_6_id,
            level,
            leaf_id
        FROM 
            flat_hierarchy fh
    ) c
    LEFT JOIN {{ df_1 }}  i ON i.id = c.level_1_id
    LEFT JOIN {{ df_1 }}  i2 ON i2.id = c.level_2_id
    LEFT JOIN {{ df_1 }}  i3 ON i3.id = c.level_3_id
    LEFT JOIN {{ df_1 }}  i4 ON i4.id = c.level_4_id
    LEFT JOIN {{ df_1 }}  i5 ON i5.id = c.level_5_id
    LEFT JOIN {{ df_1 }}  i6 ON i6.id = c.level_6_id
    ORDER BY 
        level_1_id, level_2_id, level_3_id, level_4_id, level_5_id, level_6_id
),
hazard_names as (
    SELECT DISTINCT _name as name,
    CASE 
        WHEN _name = 'Vendaval' THEN 'Gale'
        WHEN _name = 'Leishmaniose Visceral' THEN 'Visceral Leishmaniasis'
        WHEN _name = 'Deslizamento de terra' THEN 'Landslide'
        WHEN _name = 'Erosão' THEN 'Erosion'
        WHEN _name = 'Chuva' THEN 'Rain'
        WHEN _name = 'Disponiblidade' THEN 'Availability'
        WHEN _name = 'Acesso' THEN 'Access'
        WHEN _name = 'Tempestade' THEN 'Storm'
        WHEN _name = 'Seca' THEN 'Drought'
        WHEN _name = 'Malária' THEN 'Malaria'
        WHEN _name = 'Inundações, enxurradas e alagamentos' THEN 'Flooding'
        WHEN _name = 'Queimada' THEN 'Fire'
        WHEN _name = 'Aumento do Nível do Mar' THEN 'Sea Level Rise'
        WHEN _name = 'Leishmaniose Tegumentar Americana' THEN 'American Cutaneous Leishmaniasis'
        WHEN _name = 'Temperatura' THEN 'Temperature'
        WHEN _name = 'Deslizamento' THEN 'Landslide'
        WHEN _name = 'Alagamento e Inundação' THEN 'Flooding'
        ELSE null
    END AS name_en
    FROM {{df_1}}
    WHERE _LEVEL = 2
),
key_impacts as (
SELECT DISTINCT _name as name,
    CASE 
        WHEN _name = 'Recursos Hídricos' THEN 'Water Resources'
        WHEN _name = 'Segurança Alimentar' THEN 'Food Security'
        WHEN _name = 'Segurança Energética' THEN 'Energy Security'
        WHEN _name = 'Infraestrutura Portuária' THEN 'Port Infrastructure'
        WHEN _name = 'Saúde' THEN 'Public Health'
        WHEN _name = 'Desastres geo-hidrológicos' THEN 'Geo-hydrological Disasters'
        WHEN _name = 'Infraestrutura Ferroviária' THEN 'Railway Infrastructure'
        WHEN _name = 'Infraestrutura Rodoviária' THEN 'Road Infrastructure'
        ELSE null
    END AS name_en
    FROM {{df_1}}
    WHERE _LEVEL = 1
)
-- Final selection with additional scenario names split from a string
SELECT 
    c.name_en as key_impact_name,
    b.name_en as hazard_name,
    a.leaf_id as indicator_id,
    d._name as  indicator_name,
    case when a.leaf_id = a.level_3_id then 'risk score'
    when (indicator_name = 'Ameaça Climática' or indicator_name = 'Ameaça') then 'hazard score'
    when indicator_name = 'Exposição' then 'exposure score'
    when indicator_name = 'Vulnerabilidade' then 'vulnerability score'
    when indicator_name = 'Capacidade Adaptativa' then 'adaptive capacity score'
    when indicator_name = 'Sensibilidade' then 'sensitivity score'
    else null 
    end as indicator_level_name,
FROM 
    hierarchy_level a 
LEFT JOIN hazard_names b 
ON a.level_3_name = b.name
LEFT JOIN key_impacts c 
ON a.level_2_name = c.name
LEFT JOIN {{df_1}} d
ON a.leaf_id = d.id
WHERE (a.leaf_id = a.level_3_id OR 
indicator_name in ('Ameaça Climática', 'Exposição', 'Ameaça', 'Vulnerabilidade', 'Capacidade Adaptativa', 'Sensibilidade'))