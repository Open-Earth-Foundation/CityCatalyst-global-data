SELECT 
    bpc.locode, 
    STRING_AGG(DISTINCT nkbpc.gpc_reference_number, ', ') AS subsectors
FROM raw_data.brazil_pilot_cities bpc
INNER JOIN raw_data.nk_br_pilot_cities nkbpc
ON bpc.locode = nkbpc.locode
GROUP BY bpc.locode
ORDER BY bpc.locode;
