DROP TABLE IF EXISTS modelled.emissions_epe_staging;

CREATE TABLE modelled.emissions_epe_staging AS 
WITH 	state_elec_emissions AS (
SELECT 	CASE 
	    WHEN grupo = 'Rondônia' THEN 'RO'
	    WHEN grupo = 'Acre' THEN 'AC'
	    WHEN grupo = 'Amazonas' THEN 'AM'
	    WHEN grupo = 'Roraima' THEN 'RR'
	    WHEN grupo = 'Pará' THEN 'PA'
	    WHEN grupo = 'Amapá' THEN 'AP'
	    WHEN grupo = 'Tocantins' THEN 'TO'
	    WHEN grupo = 'Maranhão' THEN 'MA'
	    WHEN grupo = 'Piauí' THEN 'PI'
	    WHEN grupo = 'Ceará' THEN 'CE'
	    WHEN grupo = 'Rio Grande do Norte' THEN 'RN'
	    WHEN grupo = 'Paraíba' THEN 'PB'
	    WHEN grupo = 'Pernambuco' THEN 'PE'
	    WHEN grupo = 'Alagoas' THEN 'AL'
	    WHEN grupo = 'Sergipe' THEN 'SE'
	    WHEN grupo = 'Bahia' THEN 'BA'
	    WHEN grupo = 'Minas Gerais' THEN 'MG'
	    WHEN grupo = 'Espírito Santo' THEN 'ES'
	    WHEN grupo = 'Rio de Janeiro' THEN 'RJ'
	    WHEN grupo = 'São Paulo' THEN 'SP'
	    WHEN grupo = 'Paraná' THEN 'PR'
	    WHEN grupo = 'Santa Catarina' THEN 'SC'
	    WHEN grupo = 'Rio Grande do Sul' THEN 'RS'
	    WHEN grupo = 'Mato Grosso do Sul' THEN 'MS'
	    WHEN grupo = 'Mato Grosso' THEN 'MT'
	    WHEN grupo = 'Goiás' THEN 'GO'
	    WHEN grupo = 'Distrito Federal' THEN 'DF'
	    ELSE NULL
	END AS region_code,
	CASE
        WHEN classe = 'Poder Público' THEN 'I.2.2'
        WHEN classe = 'Rural' THEN 'I.5.2'
        WHEN classe = 'Consumo Próprio' THEN null
        WHEN classe = 'Iluminação Pública' THEN 'I.2.2'
        WHEN classe = 'Serviço Público' THEN 'I.2.2'
        WHEN classe = 'Residencial' THEN 'I.1.1'
        WHEN classe = 'Comercial' THEN 'I.2.2'
        WHEN classe = 'Industrial' THEN 'I.3.2'
        ELSE classe -- In case there are other categories not listed
    END AS gpc_reference_number,
    ano as consumption_year,
	total * 1000 as consumption_value,
	'MWh' as consumption_units,
	b.emissionfactor_value,
	b.emissionfactor_units,
	a.total * 1000 * b.emissionfactor_value * 1000 as emissions_value,
	'kg' as emissions_units,
	'CO2' as gas_name
FROM raw_data.epe_elec_consumption a 
LEFT JOIN raw_data.br_elec_ef b 
ON a.ano = b.emissionfactor_year
WHERE classe NOT IN ('Consumo Próprio', 'Total')),
epe_scaling_factor as (
SELECT 		b.locode, 
			b.city_id,
			CASE WHEN scaling_factor_description='city percentage gross value added by agriculture to state' THEN 'I.5.2'
			when scaling_factor_description='city percentage gross value added by industrial to state' THEN 'I.3.2'
			WHEN scaling_factor_description='city percentage of residential population state' THEN 'I.1.2'
			WHEN scaling_factor_description='city percentage gross value added to state' THEN 'I.2.2'
			ELSE NULL END AS gpc_reference_number,
			a.*
FROM 		raw_data.ibge_scaling_factors a 
INNER JOIN 	modelled.city_polygon b 
ON 			REPLACE(LOWER(TRIM(a.city_name)), '-', ' ') = REPLACE(LOWER(TRIM(b.city_name)), '-', ' ')
AND 		TRIM(a.region_code) = TRIM(b.region_code)
AND 		b.country_code = 'BR')
SELECT 		b.locode,
			a.region_code,
			b.city_id,
			a.gpc_reference_number,
			a.consumption_year AS emissions_year,
			SUM(a.emissions_value::numeric * factor_value::numeric) AS emissions_value,
			MAX('kg') as emissions_units,
			a.gas_name,
			SUM(a.consumption_value::numeric * factor_value::numeric) as activity_value,
			MAX('city') as spatial_granularity,
			-- activity 
			(MD5(CONCAT_WS('-', 'electricity-consumption', 'MWh'))::UUID) AS activity_id,
			MAX('electricity-consumption') as activity_name,
			MAX('MWh') as activity_units,
			-- emissionfactors
			MAX(emissionfactor_value) as emissionfactor_value,
			MAX('BRGOV') as ef_datasource_name
FROM  		state_elec_emissions a 
LEFT JOIN 	epe_scaling_factor b 
ON 			TRIM(a.region_code) = TRIM(b.region_code)
AND 		a.gpc_reference_number =b.gpc_reference_number
AND 		b.factor_year::int = (CASE WHEN a.gpc_reference_number = 'I.1.1' THEN 2022
									WHEN a.consumption_year > 2021 THEN 2022
									ELSE a.consumption_year END)
GROUP BY b.locode, a.region_code, b.city_id, a.gpc_reference_number, a.consumption_year, a.gas_name, (MD5(CONCAT_WS('-', 'electricity-consumption', 'MWh'))::UUID) 
