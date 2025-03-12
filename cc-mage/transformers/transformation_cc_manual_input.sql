DROP TABLE IF EXISTS raw_data.cc_manual_input_activity;

CREATE TABLE raw_data.cc_manual_input_activity AS
WITH input_json AS (
    SELECT
        gpc_reference_number,
        key,
        value
    FROM
        raw_data.cc_manual_input_json,
        jsonb_each(manual_input_json)
),
input_methodologies AS (
    SELECT
        gpc_reference_number,
        "key",
        jsonb_array_elements(value::jsonb) AS json_data
    FROM
        input_json
    WHERE
        key = 'methodologies'
),
input_methods_activity AS (
    SELECT
        gpc_reference_number,
        "key",
        json_data,
        json_data->>'id' AS methodology_name,
        json_data->>'inputRequired' AS activity_name,
        CASE
            WHEN jsonb_typeof(json_data->'activities') = 'array' THEN json_data->'activities'
            ELSE '[]'::jsonb -- Treat non-arrays as an empty array
        END AS activities_array
    FROM
        input_methodologies
),
input_methods_subactivity AS (
    SELECT
        gpc_reference_number,
        "key",
        json_data,
        methodology_name,
        activity_name,
        jsonb_array_elements(activities_array)->'extra-fields' AS activity_subcategories
    FROM
        input_methods_activity
),
input_methods_subactivity_expanded AS (
    SELECT
        gpc_reference_number,
        "key",
        json_data,
        methodology_name,
        activity_name,
        jsonb_array_elements(activity_subcategories) AS activity_subcategories_ex
    FROM
        input_methods_subactivity
),
input_methods_subactivity_expanded_2 AS (
    SELECT
        gpc_reference_number,
        methodology_name,
        activity_name,
        activity_subcategories_ex->>'id' AS activity_subcategory_type,
        CASE
            WHEN jsonb_typeof(activity_subcategories_ex->'options') = 'array' THEN activity_subcategories_ex->'options'
            ELSE '[]'::jsonb -- Treat non-arrays as an empty array
        END AS activity_subcategory_typename
    FROM
        input_methods_subactivity_expanded
),
input_json2 AS (
    SELECT
        gpc_reference_number,
        key,
        value
    FROM
        raw_data.cc_manual_input_json,
        jsonb_each(manual_input_json)
),
direct_methodologies AS (
    SELECT
        gpc_reference_number,
        value->>'id' AS methodology_name,
        jsonb_array_elements(value->'extra-fields') AS activity_subcategories
    FROM
        input_json2
    WHERE
        key = 'directMeasure'
),
direct_methods_subactivity_expanded AS (
    SELECT
        gpc_reference_number,
        methodology_name,
        NULL AS activity_name,
        activity_subcategories->>'id' AS activity_subcategory_type,
        CASE
            WHEN jsonb_typeof(activity_subcategories->'options') = 'array' THEN activity_subcategories->'options'
            ELSE '[]'::jsonb -- Treat non-arrays as an empty array
        END AS activity_subcategory_typename
    FROM
        direct_methodologies
),
union_methodology AS (
    SELECT
        gpc_reference_number,
        methodology_name,
        activity_name,
        activity_subcategory_type,
        REPLACE(jsonb_array_elements(activity_subcategory_typename)::varchar, '"', '') AS activity_subcategory_typename
    FROM
        input_methods_subactivity_expanded_2
    UNION
    SELECT
        gpc_reference_number,
        methodology_name,
        activity_name,
        activity_subcategory_type,
        REPLACE(jsonb_array_elements(activity_subcategory_typename)::varchar, '"', '') AS activity_subcategory_typename
    FROM
        direct_methods_subactivity_expanded
)
SELECT *
FROM union_methodology