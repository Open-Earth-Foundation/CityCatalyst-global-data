CREATE TABLE raw_data.coverage_br_pilot_cities AS
WITH dataset_coverage AS (
    -- Find covered datasets, GPC subsectors, and municipalities for 2022
    SELECT 
        large.datasource_name AS dataset,
        large.gpc_reference_number AS gpc_reference,
        STRING_AGG(DISTINCT small.municipality, ', ') AS covered_municipalities
    FROM modelled.emissions large
    INNER JOIN raw_data.brazil_pilot_cities small
    ON small.locode = large.actor_id
    WHERE large.emissions_year = 2022
    GROUP BY large.datasource_name, large.gpc_reference_number
),
missing_municipalities AS (
    -- Identify uncovered municipalities by cross-joining all datasets, subsectors, and cities
    SELECT 
        c.locode AS uncovered_locode,  -- New: Capture the city locode
        c.municipality AS uncovered_municipality,
        d.dataset,
        s.gpc_reference_number
    FROM raw_data.brazil_pilot_cities c
    CROSS JOIN (
        -- Get all distinct datasets and their covered subsectors
        SELECT DISTINCT large.datasource_name AS dataset, large.gpc_reference_number
        FROM modelled.emissions large
        WHERE large.emissions_year = 2022
    ) d
    CROSS JOIN (
        -- Get all distinct GPC subsectors in 2022
        SELECT DISTINCT gpc_reference_number FROM modelled.emissions WHERE emissions_year = 2022
    ) s
    LEFT JOIN modelled.emissions large
    ON c.locode = large.actor_id 
    AND large.datasource_name = d.dataset
    AND large.gpc_reference_number = s.gpc_reference_number
    WHERE large.actor_id IS NULL  -- Only cities that have missing data
)
SELECT 
    dc.gpc_reference AS gpc_references,
    dc.dataset,
    COALESCE(STRING_AGG(DISTINCT mm.uncovered_municipality, ', '), 'Fully Covered') AS uncovered_municipalities,  
    COALESCE(STRING_AGG(DISTINCT mm.uncovered_locode, ', '), 'Fully Covered') AS uncovered_municipalities_locode,  -- New column
    dc.covered_municipalities
FROM dataset_coverage dc
LEFT JOIN missing_municipalities mm 
ON dc.dataset = mm.dataset AND dc.gpc_reference = mm.gpc_reference_number
GROUP BY dc.gpc_reference, dc.dataset, dc.covered_municipalities
ORDER BY dc.gpc_reference, dc.dataset;