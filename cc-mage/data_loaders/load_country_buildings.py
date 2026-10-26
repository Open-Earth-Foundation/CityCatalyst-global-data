if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import importlib
import sys
from mage_ai.data_preparation.shared.secrets import get_secret_value
from mage_ai.settings.repo import get_repo_path
sys.path.insert(0, get_repo_path())
import climatetrace_country_io as _ct_io
importlib.reload(_ct_io)
from climatetrace_country_io import load_country_sector_emissions


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    kwargs = dict(kwargs)
    kwargs['aws_access_key_id'] = get_secret_value('AWS_ACCESS_KEY_ID')
    kwargs['aws_secret_access_key'] = get_secret_value('AWS_SECRET_ACCESS_KEY')
    print('CT exact-key GetObject (no S3 glob)')
    return load_country_sector_emissions('buildings', kwargs)


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
