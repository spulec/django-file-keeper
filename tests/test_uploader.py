import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(test_dir, os.path.pardir))
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

from mock import patch
import sure

from django.core import management

# @patch("keeper.core.set_key")
# def test_uploader(set_key):
#     test_filename = 'foobar.csv'

#     management.call_command('upload_data_file', test_filename, verbosity=0)

#     set_key.assert_called_with('foobar.csv')


@patch("keeper.core.get_bucket")
def test_first_upload(get_bucket):
    class FakeKey(object):
        def __init__(self, keyname):
            self.keyname = keyname
            self.contents_filename = None

        def set_contents_from_filename(self, filename):
            self.contents_filename = filename

    class FakeBucket(object):
        vals = {}
        def get_key(self, keyname):
            return self.vals.get(keyname)

        def new_key(self, keyname):
            result = FakeKey(keyname)
            self.vals[keyname] = result
            return result

    fake_bucket = FakeBucket()
    get_bucket.return_value = fake_bucket

    test_filename = 'foobar.csv'
    management.call_command('upload_data_file', test_filename, verbosity=0)

    fake_bucket.vals['foobar.csv'].contents_filename.should.equal('foobar.csv')


@patch("keeper.core.get_bucket")
@patch("keeper.core.get_input")
def test_subsequent_upload(get_input, get_bucket):
    get_input.return_value = 'Y'

    class FakeKey(object):
        def __init__(self, keyname):
            self.keyname = keyname
            self.contents_filename = None

        def set_contents_from_filename(self, filename):
            self.contents_filename = filename

    class FakeBucket(object):
        vals = {'foobar.csv': FakeKey('other.csv')}
        def get_key(self, keyname):
            return self.vals.get(keyname)

        def new_key(self, keyname):
            result = FakeKey(keyname)
            self.vals[keyname] = result
            return result

    fake_bucket = FakeBucket()
    get_bucket.return_value = fake_bucket

    test_filename = 'foobar.csv'
    management.call_command('upload_data_file', test_filename, verbosity=0)

    get_input.should.be.called_with("The file foobar.csv already exists on S3. Would you like to overwrite it[Y/N]")
    fake_bucket.vals['foobar.csv'].contents_filename.should.equal('foobar.csv')


@patch("keeper.core.get_bucket")
@patch("keeper.core.get_input")
def test_subsequent_upload_no_overwrite(get_input, get_bucket):
    get_input.return_value = 'N'

    class FakeKey(object):
        def __init__(self, keyname):
            self.keyname = keyname
            self.contents_filename = None

        def set_contents_from_filename(self, filename):
            self.contents_filename = filename

    fake_key = FakeKey('other.csv')
    fake_key.set_contents_from_filename('other.csv')

    class FakeBucket(object):
        vals = {'foobar.csv': fake_key}
        def get_key(self, keyname):
            return self.vals.get(keyname)

        def new_key(self, keyname):
            result = FakeKey(keyname)
            self.vals[keyname] = result
            return result

    fake_bucket = FakeBucket()
    get_bucket.return_value = fake_bucket

    test_filename = 'foobar.csv'
    management.call_command('upload_data_file', test_filename, verbosity=0)

    get_input.should.be.called_with("The file foobar.csv already exists on S3. Would you like to overwrite it[Y/N]")
    fake_bucket.vals['foobar.csv'].contents_filename.should.equal('other.csv')
