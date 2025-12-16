WITH city_name_data AS (
    SELECT
        trim(
            replace(
                replace(_name, ', {{country_code3}}', ''),
                'Urban Area',
                ''
            )
        ) AS city_name,
        id AS ct_cityid
    FROM raw_data.ct_cityid
)
SELECT
    a.city_name,
    a.locode,
    b.ct_cityid
FROM modelled.city_polygon AS a
JOIN city_name_data AS b
    ON trim(a.city_name) = b.city_name
WHERE a.country_code = '{{country_code2}}';