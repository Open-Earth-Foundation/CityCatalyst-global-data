WITH activity_data AS (
    SELECT DISTINCT
        activity_name,
        activity_units,
        methodology_name,
        gpc_reference_number,
        fuel_type
    FROM raw_data.ef_fuel_consumption_staging
    WHERE activity_name IS NOT NULL
)
INSERT INTO modelled.activity_subcategory (
    activity_id,
    activity_name,
    activity_units,
    gpcmethod_id,
    activity_subcategory_type
)
SELECT
    (MD5(CONCAT_WS(
        '-',
        activity_name,
        activity_units,
        CASE gpc_reference_number
            WHEN 'I.1.1' THEN jsonb_build_object('residential-building-fuel-type', fuel_type)::TEXT
            WHEN 'I.2.1' THEN jsonb_build_object('commercial-building-fuel-type', fuel_type)::TEXT
            WHEN 'I.3.1' THEN jsonb_build_object('manufacturing-and-construction-fuel-type', fuel_type)::TEXT
            WHEN 'I.4.1' THEN jsonb_build_object('energy-industries-fuel-type', fuel_type)::TEXT
            WHEN 'I.5.1' THEN jsonb_build_object('agriculture-forestry-fishing-activities-fuel-type', fuel_type)::TEXT
            WHEN 'I.6.1' THEN jsonb_build_object('non-specific-sources-fuel-type', fuel_type)::TEXT
            ELSE jsonb_build_object('fuel_type', fuel_type)::TEXT
        END,
        MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::TEXT
    ))::UUID) AS activity_id,
    activity_name,
    activity_units,
    MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID AS gpcmethod_id,
    CASE gpc_reference_number
        WHEN 'I.1.1' THEN jsonb_build_object('residential-building-fuel-type', fuel_type)
        WHEN 'I.2.1' THEN jsonb_build_object('commercial-building-fuel-type', fuel_type)
        WHEN 'I.3.1' THEN jsonb_build_object('manufacturing-and-construction-fuel-type', fuel_type)
        WHEN 'I.4.1' THEN jsonb_build_object('energy-industries-fuel-type', fuel_type)
        WHEN 'I.5.1' THEN jsonb_build_object('agriculture-forestry-fishing-activities-fuel-type', fuel_type)
        WHEN 'I.6.1' THEN jsonb_build_object('non-specific-sources-fuel-type', fuel_type)
        
        ELSE jsonb_build_object('fuel_type', fuel_type)
    END AS activity_subcategory_type
FROM activity_data
ON CONFLICT (activity_id) DO UPDATE SET
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;