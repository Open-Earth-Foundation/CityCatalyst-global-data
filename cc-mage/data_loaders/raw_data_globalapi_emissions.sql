DROP TABLE IF EXISTS raw_data.globalapi_emissions_co2eq;

CREATE TABLE raw_data.globalapi_emissions_co2eq AS 
SELECT e.actor_id as locode, e.gpc_reference_number, e.datasource_name, e.emissions_year,
		'co2eq' as gas_name,
       COALESCE(sum(e.emissions_value * gwp.ar5),0) as emissions_value
FROM modelled.emissions e
LEFT JOIN 	modelled.global_warming_potential gwp
ON 			(CASE WHEN upper(e.gas_name) = 'CH4' THEN
             CASE WHEN e.gpc_reference_number LIKE 'I.5%' OR e.gpc_reference_number LIKE 'III.%' OR e.gpc_reference_number LIKE 'V%' THEN 'CH4nonfossil'
             ELSE 'CH4fossil' END
             ELSE upper(e.gas_name) END)  = gwp.gas_name
AND 		gwp.time_horizon = '100 year'
WHERE UPPER(e.gas_name) IN ('CO2','CH4','N2O')
AND e.spatial_granularity = 'city' 
GROUP BY e.actor_id, e.gpc_reference_number, e.datasource_name, e.emissions_year
;