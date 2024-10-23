SELECT  
        STRING_SPLIT(a._name, '/')[1] AS city_name,
        STRING_SPLIT(a._name, '/')[2] AS region,
        b.key_impact_name,
        b.hazard_name,
        CASE 
        WHEN scenario_id IS NULL THEN 'current'
        WHEN scenario_id = 1 THEN 'optimistic'
        WHEN scenario_id = 2 THEN 'pesimistic'
        ELSE NULL 
    END AS scenario_name,
    indicator_level_name,
    _value indicator_value,
    _year indicator_year
FROM {{ df_1 }} a
INNER JOIN target_indicator b 
ON a.indicator_id = b.indicator_id
WHERE _value >= 0