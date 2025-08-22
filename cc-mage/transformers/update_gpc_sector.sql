INSERT INTO modelled.gpc_sector 
    (sector_name, subsector_name, sector_refno, subsector_refno, scope, gpc_reference_number, reporting_level, gpc_version)
SELECT  sector as sector_name, 
        subsector as subsector_name, 
        sector_refno, 
        subsector_refno, 
        _scope as scope, 
        coalesce(subcategory_refno,subsector_refno)  as gpc_reference_number, 
        reporting_level, 
        gpc_version
from raw_data.gpc_sector
ON CONFLICT (gpc_reference_number)
DO UPDATE SET 
    sector_name = EXCLUDED.sector_name,
    subsector_name = EXCLUDED.subsector_name,
    sector_refno = EXCLUDED.sector_refno,
    subsector_refno = EXCLUDED.subsector_refno,
    scope = EXCLUDED.scope,
    reporting_level = EXCLUDED.reporting_level,
    gpc_version = EXCLUDED.gpc_version
    ;