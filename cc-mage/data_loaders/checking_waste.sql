WITH locodes_split AS (
    -- Step 1: Split uncovered_municipalities_locode into separate rows
    SELECT DISTINCT  
        cpc.gpc_references AS gpc_reference_number,  
        unnest(string_to_array(cpc.uncovered_municipalities_locode, ', ')) AS individual_locode
    FROM raw_data.coverage_br_pilot_cities cpc
),
gpc_III11 AS (
    -- Step 2: Get uncovered locodes for GPC reference III.1.1
    SELECT DISTINCT individual_locode
    FROM locodes_split
    WHERE gpc_reference_number = 'III.1.1'
),
gpc_III12 AS (
    -- Step 3: Get uncovered locodes for GPC reference III.1.2
    SELECT DISTINCT individual_locode
    FROM locodes_split
    WHERE gpc_reference_number = 'III.1.2'
),
gpc_III31 AS (
    -- Step 4: Get uncovered locodes for GPC reference III.3.1
    SELECT DISTINCT individual_locode
    FROM locodes_split
    WHERE gpc_reference_number = 'III.3.1'
),
gpc_III32 AS (
    -- Step 5: Get uncovered locodes for GPC reference III.3.2
    SELECT DISTINCT individual_locode
    FROM locodes_split
    WHERE gpc_reference_number = 'III.3.2'
)
-- Step 6: Compare within matching GPC groups only and filter only matching locodes
SELECT DISTINCT  
    gIII11.individual_locode AS city_locode,
    'Present in both III.1.1 and III.1.2' AS city_status
FROM gpc_III11 gIII11
INNER JOIN gpc_III12 gIII12 ON gIII11.individual_locode = gIII12.individual_locode

UNION ALL

SELECT DISTINCT  
    gIII31.individual_locode AS city_locode,
    'Present in both III.3.1 and III.3.2' AS city_status
FROM gpc_III31 gIII31
INNER JOIN gpc_III32 gIII32 ON gIII31.individual_locode = gIII32.individual_locode

ORDER BY city_locode;

