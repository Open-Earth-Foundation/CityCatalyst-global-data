DROP TABLE IF EXISTS raw_data.globalapi_activity_translated;

CREATE TABLE raw_data.globalapi_activity_translated AS 
WITH activity_details AS (
    SELECT
        activity_name,
        key,
        value
    FROM
        modelled.activity_subcategory,
        json_each(activity_subcategory_type) -- Use json_each for json type
),
activity_flattened as (
SELECT DISTINCT
    activity_name,
    a.key AS subcategory_type,
    REPLACE(a.value::text, '"', '') AS subcategory_typename
FROM
    activity_details a
WHERE
    key NOT LIKE 'activity_subcategory%'
    AND key NOT LIKE 'data-source'
ORDER BY
    activity_name
),
all_translation_string AS (
SELECT
    'activity_name' AS activity_reference,
    a.activity_name AS activity_reference_string,
    CASE WHEN b.translation_string IS NOT NULL THEN 'Y' ELSE 'N' END AS string_exists_cc
FROM
    activity_flattened a
LEFT JOIN
    raw_data.cc_translation_string b
ON
    a.activity_name = b.translation_string
UNION ALL
SELECT
    'subcategory_type' AS activity_reference,
    a.subcategory_type AS activity_reference_string,
    CASE WHEN c.translation_string IS NOT NULL THEN 'Y' ELSE 'N' END AS string_exists_cc
FROM
    activity_flattened a
LEFT JOIN
    raw_data.cc_translation_string c
ON
    a.subcategory_type = c.translation_string
UNION ALL
SELECT
    'subcategory_typename' AS activity_reference,
    a.subcategory_typename AS activity_reference_string,
    CASE WHEN d.translation_string IS NOT NULL THEN 'Y' ELSE 'N' END AS string_exists_cc
FROM
    activity_flattened a
LEFT JOIN
    raw_data.cc_translation_string d
ON
    a.subcategory_typename = d.translation_string
    )
SELECT *
FROM all_translation_string
WHERE string_exists_cc = 'N'