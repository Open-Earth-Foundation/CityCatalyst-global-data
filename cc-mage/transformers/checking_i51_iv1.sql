WITH locodes_split AS (
    -- Step 1: Split uncovered_municipalities_locode into separate rows
    SELECT DISTINCT  
        cpc.gpc_references AS gpc_reference_number,  
        unnest(string_to_array(cpc.uncovered_municipalities_locode, ', ')) AS individual_locode
    FROM raw_data.coverage_br_pilot_cities cpc
),
gpc_151 AS (
    -- Step 2: Get DISTINCT uncovered cities for GPC reference I.5.1
    SELECT DISTINCT individual_locode
    FROM locodes_split
    WHERE gpc_reference_number = 'I.5.1'
),
gpc_V1 AS (
    -- Step 3: Get DISTINCT uncovered cities for GPC reference V.1
    SELECT DISTINCT individual_locode
    FROM locodes_split
    WHERE gpc_reference_number = 'V.1'
),
gpc_V2 AS (
    -- Step 4: Get DISTINCT uncovered cities for GPC reference V.2
    SELECT DISTINCT individual_locode
    FROM locodes_split
    WHERE gpc_reference_number = 'V.2'
),
gpc_V3 AS (
    -- Step 5: Get DISTINCT uncovered cities for GPC reference V.3
    SELECT DISTINCT individual_locode
    FROM locodes_split
    WHERE gpc_reference_number = 'V.3'
)
-- Step 6: Compare all sets to find missing and common locodes
SELECT DISTINCT  
    ls.individual_locode AS city_locode,
    CASE 
        WHEN g151.individual_locode IS NOT NULL AND gV1.individual_locode IS NOT NULL THEN 'Present in both I.5.1 and V.1'
        WHEN g151.individual_locode IS NOT NULL AND gV2.individual_locode IS NOT NULL THEN 'Present in both I.5.1 and V.2'
        WHEN g151.individual_locode IS NOT NULL AND gV3.individual_locode IS NOT NULL THEN 'Present in both I.5.1 and V.3'
        WHEN g151.individual_locode IS NOT NULL AND gV1.individual_locode IS NULL AND gV2.individual_locode IS NULL AND gV3.individual_locode IS NULL THEN 'Only in I.5.1'
        WHEN g151.individual_locode IS NULL AND (gV1.individual_locode IS NOT NULL OR gV2.individual_locode IS NOT NULL OR gV3.individual_locode IS NOT NULL) THEN 'In V.1, V.2, or V.3 but missing in I.5.1'
    END AS city_status
FROM locodes_split ls
LEFT JOIN gpc_151 g151 ON ls.individual_locode = g151.individual_locode
LEFT JOIN gpc_V1 gV1 ON ls.individual_locode = gV1.individual_locode
LEFT JOIN gpc_V2 gV2 ON ls.individual_locode = gV2.individual_locode
LEFT JOIN gpc_V3 gV3 ON ls.individual_locode = gV3.individual_locode
WHERE g151.individual_locode IS NOT NULL OR gV1.individual_locode IS NOT NULL OR gV2.individual_locode IS NOT NULL OR gV3.individual_locode IS NOT NULL
ORDER BY city_locode;


