WITH activity_data AS (
    SELECT DISTINCT
        activity_name,
        activity_units,
        methodology_name,
        gpc_reference_number
    FROM raw_data.biolog_treatment_eurostats_staging
    WHERE activity_name IS NOT NULL
)
INSERT INTO modelled.activity_subcategory (
    activity_id, 
    activity_name, 
    activity_units, 
    gpcmethod_id, 
    activity_subcategory_type
)
SELECT DISTINCT
    -- Build activity_id using activity info + derived gpcmethod_id
    MD5(CONCAT_WS(
        '-',
        activity_name,
        activity_units,
        jsonb_build_object(
            'biological-treatment-inboundary-waste-state', 'waste-state-wet-waste',
            'biological-treatment-inboundary-treatment-type', 'treatment-type-composting'
        )::TEXT,
        MD5(CONCAT_WS(
            '-',
            methodology_name,
            gpc_reference_number
        ))::TEXT
    ))::UUID AS activity_id,

    activity_name,
    activity_units,

    -- Build gpcmethod_id from methodology_name + gpc_reference_number
    MD5(CONCAT_WS(
        '-',
        methodology_name,
        gpc_reference_number
    ))::UUID AS gpcmethod_id,

    jsonb_build_object(
        'biological-treatment-inboundary-waste-state', 'waste-state-wet-waste',
        'biological-treatment-inboundary-treatment-type', 'treatment-type-composting'
    ) AS activity_subcategory_type

FROM activity_data

ON CONFLICT (activity_id) DO UPDATE SET
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;
