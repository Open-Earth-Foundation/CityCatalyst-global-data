from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_postgres(*args, **kwargs):
    """
    Template for loading data from a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    query = '''select locode, lat, lon
                from modelled.city_polygon cp 
                where locode in ('BR SER', 'BR RBR', 'BR CXL', 'BR CMG', 'BR MGE', 'BR ATB', 'BR ATM', 'BR ACZ', 'BR ARC', 'BR BVB', 'BR CCX', 'BR CAJ', 'BR CME', 'BR CMA', 'BR CGR', 'BR CLO', 'BR CCY', 'BR CII', 'BR CGE', 'BR COX', 'BR CAT', 'BR CZL', 'BR CBA', 'BR FMO', 'BR FOR', 'BR GYN', 'BR GRA', 'BR IOS', 'BR IIP', 'BR JPR', 'BR JZO', 'BR MAO', 'BR MRD', 'BR MOC', 'BR MOS', 'BR PIS', 'BR PIN', 'BR PES', 'BR POA', 'BR RNV', 'BR RIO', 'BR SCV', 'BR SJM', 'BR SLO', 'BR SIN', 'BR SOB', 'BR SOR', 'BR TSE', 'BR TAA', 'BR VDS')
            '''  
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        return loader.load(query)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
