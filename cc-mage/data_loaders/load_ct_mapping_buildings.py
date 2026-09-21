if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from climatetrace_country_io import load_ct_sector_mapping


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    return load_ct_sector_mapping('buildings', kwargs)


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
