import pandas as pd
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    """
    Template for loading data from a S3 bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#s3
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = kwargs['bucket_name']
    object_key = 'files/ccra/adapta_brazil/adapta_city_api_response.csv'

    df = S3.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )
    
    filtered_df = df[(df['indicator_name'].isin([
                        'Índice de precipitação-evapotranspiração padronizado', 
                        'Dias consecutivos secos', 
                        'Deslizamento de terra', 
                        'Domicílios em áreas de risco',
                        'Índice de Ameaça de inundações, enxurradas e alagamentos', 
                        'Pobreza energética',
                        'Temperatura máxima', 
                        'Produção e comercialização de alimentos', 
                        'Dependência da irrigação em grande escala',
                        #'Produção e comercialização',
                        #'Densidade de estabelecimentos agropecuários',
                        'Máxima precipitação anual em cinco dias consecutivos',
                        'Precipitação total anual acima do percentil 95'
                        ])) | (df['indicator_id'].isin([5047, 5006, 5018, 7548, 7549]))]

    # 5 is for food security
    #filtered_df = df[df['indicator_id'].isin([5047])]

    return filtered_df


@test
def test_output(output, *args) -> None:
    """
    Test that we get both the indicator names
    """
    unique_indicators = output['indicator_name'].unique()
    assert len(unique_indicators) > 5, (
        f"Expected 2 unique indicator names, but found {len(unique_indicators)}: {unique_indicators}"
    )
