WITH locodes_split AS (
    -- Step 1: Split uncovered_municipalities_locode into separate rows
    SELECT 
        cpc.dataset,  
        cpc.gpc_references AS gpc_reference_number,  
        unnest(string_to_array(cpc.uncovered_municipalities_locode, ', ')) AS individual_locode
    FROM raw_data.coverage_br_pilot_cities cpc
),
filtered_results AS (
    -- Step 2: Join with modelled.nk_br_pilot_cities and keep only matching gpc_reference_number
    SELECT DISTINCT 
        nkbpc.locode,  -- Group by locode
        ls.gpc_reference_number
    FROM locodes_split ls
    INNER JOIN raw_data.nk_br_pilot_cities nkbpc
    ON ls.individual_locode = nkbpc.locode
    AND ls.gpc_reference_number = nkbpc.gpc_reference_number
    WHERE ls.dataset NOT IN ('ClimateTRACEv2023', 'SEEG')  -- Exclude specific datasets
)
SELECT 
    fr.locode,
    STRING_AGG(DISTINCT fr.gpc_reference_number, ', ') AS unique_gpc_references  -- Aggregate unique GPCs per city
FROM filtered_results fr
GROUP BY fr.locode
ORDER BY fr.locode;
