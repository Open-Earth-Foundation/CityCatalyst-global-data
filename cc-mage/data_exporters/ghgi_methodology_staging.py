from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(**kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'raw_data'  
    table_name = 'ghgi_methodology_staging'  
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    methodology = {
        "methodology_name": "fuel-combustion-consumption",
        "methodology_description": "The Fuel Consumption methodology is a Tier 1 IPCC approach used in the GPC to estimate Scope 1 emissions from stationary energy by calculating GHG emissions based on the quantity of fuel consumed in buildings, industry, and other fixed sources within the city boundary. It directly links fuel usage to combustion emissions and is recommended when disaggregated fuel data by type and subsector are available.",
    }

    gpc_reference_numbers = ["I.1.1", "I.2.1", "I.3.1", "I.4.1", "I.5.1", "I.6.1"]

    # Create a list of dictionaries, one for each gpc_reference_number
    rows = [
        {**methodology, "gpc_reference_number": gpc_ref}
        for gpc_ref in gpc_reference_numbers
    ]

    # Create DataFrame
    df = pd.DataFrame(rows)

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  
            if_exists='replace',  
        )