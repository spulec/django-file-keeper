import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(test_dir, os.path.pardir))
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

from mock import patch
import sure

from django.core import management

from keeper.core import use_file


@patch("keeper.core.set_key")
def test_uploader(set_key):
    test_filename = 'foobar.csv'

    management.call_command('upload_data_file', test_filename, verbosity=0)

    set_key.assert_called_with('foobar.csv')
