if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, data_2, *args, **kwargs):
    country_name1 = 'Germany'
    df1 = data_2['Table 1']
    df2 = data_2['Table 2']
    gdf = data

    #-------------------------------
    # cleaning df1
    df1 = df1.iloc[6:43, :9]
    df1.columns = ['country_code', 'country_name', '1995', '2000', '2005', '2010', '2015', '2020', '2023']
    # cleaning country names
    df1['country_name'] = df1['country_name'].str.replace(r'\s*\([^)]*\)\s*', '', regex=True).str.strip()
    df1.loc[df1['country_code'] == 'EL', 'country_code'] = 'GR'
    # filtering the df for a specific year
    df_2023 = df1[['country_code', 'country_name', '2023']]

    #-------------------------------
    # cleaning df2
    df2 = df2.iloc[9:13, 1:-1]
    df2.columns = ['management', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', 
                    '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', 
                    '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    # Get the year columns (all columns except 'management')
    year_columns = df2.columns.drop('management')
    # Calculate percentages: each value / column total
    df_pct = df2.copy()
    df_pct[year_columns] = df2[year_columns].div(df2[year_columns].sum())
    # filtering df2 for a specific year
    df_management = df_pct[['management', '2023']]

    #-------------------------------
    # combining waste per capita and management fraction
    result = df_2023.merge(df_management, how='cross')
    # Rename columns for clarity
    result = result.rename(columns={
        '2023_x': 'waste_per_capita_kg',
        '2023_y': 'management_fraction'
    })
    # Calculate waste amount for each management type per country
    result['waste_amount'] = result['waste_per_capita_kg'] * result['management_fraction']

    # Reorder columns for readability
    result = result[['country_code', 'country_name', 'management', 'waste_per_capita_kg', 'management_fraction', 'waste_amount']]

    result['units'] = 'kg'

    # filtering just for one country
    df_country = result[result['country_code'] == 'DE']

    # combining with pop data
    # Cross join: Each polygon gets all 4 management types
    result_gdf = gdf.merge(df_country[['management', 'waste_per_capita_kg', 'management_fraction', 'waste_amount', 'units']], how='cross')

    # Calculate total waste for each polygon and management type
    result_gdf['total_waste'] = result_gdf['population'] * result_gdf['waste_amount']

    # Reorder columns for clarity
    result_gdf = result_gdf[['city_id', 'locode', 'country_code', 'population', 'management', 'waste_amount', 
                            'total_waste', 'units', 'scope']]

    return result_gdf


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
