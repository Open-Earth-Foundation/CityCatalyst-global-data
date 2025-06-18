WITH activity_data AS (
    SELECT DISTINCT
        activity_name,
        activity_units,
        methodology_name,
        gpc_refno AS gpc_reference_number,
        source_name,
        "livestock_species",
        "livestock_activity_type",
        "livestock_subactivity_type",
        MD5(CONCAT_WS('-', methodology_name, gpc_refno))::UUID AS method_id
    FROM raw_data.ct_staging
    WHERE activity_name IS NOT NULL
)
INSERT INTO modelled.activity_subcategory (
    activity_id, 
    activity_name, 
    activity_units, 
    method_id, 
    activity_subcategory_type
)
SELECT DISTINCT
    MD5(CONCAT_WS(
        '-',
        activity_name,
        activity_units,
        jsonb_build_object(
            'data-source', source_name,
            'livestock-species', livestock_species,
            'livestock-activity-type', livestock_activity_type,
            'livestock-subactivity-type', livestock_subactivity_type
        )::TEXT,
        method_id::TEXT
    ))::UUID AS activity_id,
    activity_name,
    activity_units,
    method_id,
    jsonb_build_object(
        'data-source', source_name,
        'livestock-species', livestock_species,
        'livestock-activity-type', livestock_activity_type,
        'livestock-subactivity-type', livestock_subactivity_type
    ) AS activity_subcategory_type
FROM activity_data
ON CONFLICT (activity_id) DO UPDATE SET
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    method_id = EXCLUDED.method_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;