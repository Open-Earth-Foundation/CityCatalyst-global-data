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


    values = []
    for key, val in dic_methodologies.items():
        gpc_refno = val['gpc_refno']
        methodology_name = val['methodology_name']
        methodology_description = val['methodology_description']
        scope = val['scope']
        gpcmethod_id = f"MD5(CONCAT_WS('-', '{gpc_refno}', '{methodology_name}', '{methodology_description}', {scope}))::UUID"
        values.append(f"({gpcmethod_id}, '{gpc_refno}', '{methodology_name}', '{methodology_description}', {scope})")

    query = f"""
    INSERT INTO modelled.gpc_methodology (gpcmethod_id, gpc_refno, methodology_name, methodology_description, scope)
    VALUES {', '.join(values)}
    ON CONFLICT (gpcmethod_id)
    DO UPDATE SET 
        gpc_refno = EXCLUDED.gpc_refno,
        methodology_name = EXCLUDED.methodology_name,
        methodology_description = EXCLUDED.methodology_description,
        scope = EXCLUDED.scope;
    """
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
