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

    methodology = [
        {
            "methodology_name": "methane-commitment-solid-waste-inboundary-methodology",
            "methodology_description": "The Methane Commitment methodology is a Tier 1 approach from the 2006 IPCC Guidelines endorsed by the GPC (v.07), used to estimate CH₄ emissions from municipal solid waste disposal. It assumes that all degradable organic carbon (DOC) will eventually decompose and attributes 100% of methane emissions to the year of waste deposition, simplifying the estimation for cities lacking detailed time-series data.",
            "gpc_reference_number": 'III.1.1'
        },
        {
            "methodology_name": "methane-commitment-solid-waste-outboundary-methodology",
            "methodology_description": "The Methane Commitment methodology is a Tier 1 approach from the 2006 IPCC Guidelines endorsed by the GPC (v.07), used to estimate CH₄ emissions from municipal solid waste disposal. It assumes that all degradable organic carbon (DOC) will eventually decompose and attributes 100% of methane emissions to the year of waste deposition, simplifying the estimation for cities lacking detailed time-series data.",
            "gpc_reference_number": 'III.1.2'
        }
    ]

    # Create DataFrame
    df = pd.DataFrame(methodology)

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  
            if_exists='replace',  
        )