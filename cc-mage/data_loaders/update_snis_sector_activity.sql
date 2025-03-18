WITH subcategories AS ( 
    SELECT DISTINCT 
        (MD5(CONCAT_WS('-', activity_name, gpcmethod_id, income_group, treatment_type, treatment_status, collection_status))::UUID) AS activity_id,
        activity_name,
        activity_units,                         
        gpcmethod_id::uuid as gpcmethod_id,
        income_group, 
        treatment_type, 
        treatment_status, 
        collection_status
    FROM 
        modelled.snis_staging
    WHERE activity_name IS NOT NULL
),
final_subcategories AS (
    SELECT 
        activity_id,
        activity_name,
        activity_units,                         
        gpcmethod_id,             
        json_build_object(
            'wastewater-inside-domestic-calculator-income-group', income_group,
            'wastewater-inside-domestic-calculator-treatment-name', treatment_type,
            'wastewater-inside-domestic-calculator-treatment-status', treatment_status,
            'wastewater-inside-domestic-calculator-collection-status', collection_status
        ) AS activity_subcategory_type
    FROM 
        subcategories
)
INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT 
    activity_id,
    activity_name,
    activity_units,                         
    gpcmethod_id,             
    activity_subcategory_type        
FROM 
    final_subcategories
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;