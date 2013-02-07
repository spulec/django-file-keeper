import boto
from mock import patch
import sure

from keeper.core import get_bucket, use_file

@patch("keeper.core.Keeper.get_file")
def test_basic_decorator(get_file):
    get_file.return_value = ["test1", "test2"]

    @use_file('foobar.csv')
    def a_handle(the_file, *args, **options):
        lines = []
        for line in the_file:
            lines.append(line)
        return lines

    a_handle.when.called_with().should.return_value(["test1", "test2"])


@patch("keeper.core.get_bucket")
def test_key_doesnt_exist(get_bucket):
    get_bucket.return_value.get_key.return_value = None

    @use_file('foobar.csv')
    def a_handle(the_file, *args, **options):
        pass

    a_handle.when.called_with().should.throw(IOError,
        'The file foobar.csv cannot be found on S3.')


@patch("keeper.core.settings")
@patch("keeper.core.boto.connect_s3")
def test_get_bucket(connect_s3, settings):
    connect_s3.return_value.get_bucket.return_value = "foobar"
    get_bucket.when.called_with().should.return_value("foobar")
