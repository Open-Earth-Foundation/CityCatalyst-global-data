WITH update_data AS (
    SELECT DISTINCT
        activity_id,
        activity_name,
        activity_units,
        method_id AS gpcmethod_id, -- corrected to match activity_id if necessary
        income_group,
        treatment_type,
        treatment_status,
        collection_status
    FROM raw_data.ct_wastewater_emissions_staging
)
INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT 
    activity_id,
    activity_name,
    activity_units,
    gpcmethod_id,
    jsonb_build_object(
        'wastewater-inside-domestic-calculator-income-group', income_group,
        'wastewater-inside-domestic-calculator-treatment-name', treatment_type,
        'wastewater-inside-domestic-calculator-treatment-status', treatment_status,
        'wastewater-inside-domestic-calculator-collection-status', collection_status
    ) AS activity_subcategory_type
FROM update_data
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;