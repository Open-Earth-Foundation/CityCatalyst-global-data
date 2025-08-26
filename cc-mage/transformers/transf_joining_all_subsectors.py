if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from pandas import DataFrame

@transformer
def transform(data: DataFrame, data_2: DataFrame, data_3: DataFrame, data_4: DataFrame, *args, **kwargs):
    """
    """
    # diccionary to map fuel names with fuel ids
    fuel_to_fuel_ids_mapping = {
        'Anthracite': 'fuel-type-anthracite',
        'Aviation Gasoline': 'fuel-type-aviation-gasoline',
        'Aviation gasoline': 'fuel-type-aviation-gasoline', 
        'Biodiesels': 'fuel-type-biodiesel',
        'Biogasoline': 'fuel-type-biogasoline',
        'Bitumen': 'fuel-type-bitumen',
        'Blast Furnace Gas': 'fuel-type-blast-furnace-gas',
        'Brown Coal Briquettes': 'fuel-type-brown-coal-briquettes',
        'Butane': 'fuel-type-butane', 
        'Charcoal': 'fuel-type-charcoal',
        'Coal (manufactured solid fuels)': 'fuel-type-coal',
        'Coal Tar': 'fuel-type-coal-tar',
        'Coal (Bituminous or Black coal)': 'fuel-type-bituminous-coal', 
        'Coke Oven Coke and Lignite Coke': 'fuel-type-coke-oven-coke-lignite-coke',
        'Coke': 'fuel-type-coke-oven-coke-lignite-coke',
        'Coke Oven Gas': 'fuel-type-coke-oven-gas',
        'Coking Coal': 'fuel-type-coking-coal',
        'Coking coal': 'fuel-type-coking-coal', 
        'Compressed Natural Gas (CNG)': 'fuel-type-natural-gas',
        'Crude Oil': 'fuel-type-crude-oil',
        'Crude oil': 'fuel-type-crude-oil', 
        'Diesel Oil': 'fuel-type-diesel-oil',
        'Diesel oil': 'fuel-type-diesel-oil', 
        'Ethane': 'fuel-type-ethane',
        'Ethanol': 'fuel-type-ethanol', 
        'E85': 'fuel-type-e85',
        'Gas Coke': 'fuel-type-gas-coke',
        'Gas Oil': 'fuel-type-gas-oil',
        'Gas oil': 'fuel-type-gas-oil',
        'Hydrogen': 'fuel-type-hydrogen', 
        'Industrial Wastes': 'fuel-type-industrial-wastes',
        'Jet Gasoline': 'fuel-type-jet-gasoline',
        'Jet gasoline': 'fuel-type-jet-gasoline', 
        'Jet Kerosene': 'fuel-type-jet-kerosene',
        'Jet kerosene': 'fuel-type-jet-kerosene',
        'Kerosene': 'fuel-type-kerosene', 
        'Landfill Gas': 'fuel-type-landfill-gas',
        'Landfill gas': 'fuel-type-landfill-gas', 
        'Lignite': 'fuel-type-lignite',
        'Liquefied Natural Gas (LNG)': 'fuel-type-natural-gas-liquids',
        'Liquefied Petroleum Gases': 'fuel-type-liquefied-petroleum-gases',
        'Liquefied Petroleum Gas (LPG)': 'fuel-type-liquefied-petroleum-gases', 
        'Lubricants': 'fuel-type-lubricants',
        'Methanol': 'fuel-type-methanol',
        'Motor Gasoline': 'fuel-type-gasoline',
        'Motor gasoline (petrol)': 'fuel-type-gasoline', 
        'Municipal wastes (all)': 'fuel-type-municipal-waste',
        'Municipal Wastes (biomass fraction)': 'fuel-type-municipal-waste-biomass-fraction',
        'Municipal wastes (biomass fraction)': 'fuel-type-municipal-waste-biomass-fraction', 
        'Municipal Wastes (non-biomass fraction)': 'fuel-type-municipal-wastes-non-biomass-fraction',
        'Municipal wastes (non-biomass fraction)': 'fuel-type-municipal-wastes-non-biomass-fraction',
        'Naphtha': 'fuel-type-naphtha',
        'Natural Gas': 'fuel-type-natural-gas',
        'Natural gas': 'fuel-type-natural-gas',
        'Natural Gas Liquids\n(NGLs)': 'fuel-type-natural-gas-liquids',
        'Shale Oil': 'fuel-type-shale-oil',
        'Oil Shale and Tar Sands': 'fuel-type-shale-oil-tar-sands',
        'Orimulsion': 'fuel-type-orimulsion',
        'Other Biogas': 'fuel-type-biogas',
        'Other biogas': 'fuel-type-biogas', 
        'Other Bituminous Coal': 'fuel-type-other-bituminous-coal',
        'Other Kerosene': 'fuel-type-other-kerosene',
        'Other Liquid Biofuels': 'fuel-type-biofuel',
        'Other Liquid BioFuels': 'fuel-type-biofuel', 
        'Other Petroleum Products': 'fuel-type-other-petroleum-products',
        'Other Primary Solid Biomass': 'fuel-type-other-primary-solid-biomass',
        'Oxygen Steel Furnace Gas': 'fuel-type-oxygen-steel-furnace-gas',
        'Patent Fuel': 'fuel-type-patent-fuel',
        'Peat': 'fuel-type-peat',
        'Petroleum Coke': 'fuel-type-petroleum-coke',
        'Petroleum coke': 'fuel-type-petroleum-coke',
        'Propane': 'fuel-type-propane', 
        'Refinery Feedstocks': 'fuel-type-refinery-feedstocks',
        'Refinery Gas': 'fuel-type-refinery-gas',
        'Residual Fuel Oil': 'fuel-type-residual-fuel-oil',
        'Residual fuel oil': 'fuel-type-residual-fuel-oil', 
        'Sewage sludge': 'fuel-type-sewage-sludge', 
        'Sludge Gas': 'fuel-type-sludge-gas',
        'Sludge gas': 'fuel-type-sludge-gas',
        'Sub-Bituminous Coal': 'fuel-type-sub-bituminous-coal',
        'Waste Oils': 'fuel-type-waste-oils',
        'Wood/Wood Waste': 'fuel-type-wood-wood-waste',
        'firewood': 'fuel-type-firewood'
    }

    # filter by units
    conversion_factor_vol = data[(data['To'] == 'TJ') & (data['From '] == 'm³')]
    conversion_factor_mass = data_2[(data_2['To'] == 'TJ') & (data_2['From '] == 'kg')]

    # concant dfs with EF values
    EF_final = pd.concat([data_3, data_4], ignore_index=True)

    # assign fuel ids based on fuel names
    EF_final['fuel_type'] = EF_final['fuel'].map(fuel_to_fuel_ids_mapping)

    # drop EF without an ID
    EF_final = EF_final.dropna(subset=['fuel_type'])

    # apply conversion of energy to volumen only for gas and liquid fuels
    tmp = EF_final.merge(conversion_factor_vol[['fuel_type', 'Factor', 'From ']], on='fuel_type', how='left')
    tmp.dropna(subset=['Factor'], inplace=True)
    tmp['emissions_per_activity'] = tmp['value'] * tmp['Factor']
    tmp['units_after_transformation'] = 'kg/m3' # kg of gas / m3 of fuel
    tmp['activity_units'] = 'm3'

    # apply conversion of energy to mass only for solid fuels
    tmp2 = EF_final.merge(conversion_factor_mass[['fuel_type', 'Factor', 'From ']], on='fuel_type', how='left')
    tmp2.dropna(subset=['Factor'], inplace=True)
    tmp2['emissions_per_activity'] = tmp2['value'] * tmp2['Factor']
    tmp2['units_after_transformation'] = 'kg/kg' # kg of gas / kg of fuel
    tmp2['activity_units'] = 'kg'

    EF_final = pd.concat([tmp, tmp2], ignore_index=True)

    # Define the mapping dictionary
    methodology_mapping = {
        'I.1.1': 'fuel-combustion-residential-buildings-methodology',
        'I.2.1': 'fuel-combustion-commercial-buildings-methodology',
        'I.3.1': 'fuel-combustion-manufacturing-and-construction-methodology',
        'I.4.1': 'fuel-combustion-energy-industries-methodology',
        'I.5.1': 'fuel-combustion-agriculture-forestry-fishing-activities-methodology',
        'I.6.1': 'fuel-combustion-non-specific-sources-methodology'
    }
    EF_final['methodology_name'] = EF_final['gpc_reference_number'].map(methodology_mapping)

    EF_final['actor_id'] = 'world'
    EF_final['active_to'] = ''
    EF_final['active_from'] = ''
    EF_final['activity_name'] = 'fuel-consumption'
    EF_final['publisher_name'] = 'IPCC'
    EF_final['datasource_name'] = 'IPCC'
    EF_final['dataset_name'] = 'IPCC Emission Factor Database (EFDB) [2006 IPCC Guidelines]'
    EF_final['publisher_url'] = 'https://www.ipcc.ch/'
    EF_final['dataset_url'] = 'https://www.ipcc-nggip.iges.or.jp/EFDB/main.php'



    EF_final.drop(columns=[
        'EF ID', 
        'ipcc_2006_category', 
        'fuel', 
        'Description', 
        'units', 
        'equation', 
        'value_min', 
        'value_max', 
        'Factor', 
        'From ',
        'value'
        ], inplace=True)

    EF_final.rename(columns={
        'units_after_transformation': 'units'
    }, inplace=True)

    return EF_final


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'