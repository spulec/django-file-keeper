from mock import mock_open, patch
import sure

from keeper.core import get_bucket, use_file

@patch("keeper.core.get_bucket")
def test_basic_decorator(get_bucket):
    class FakeKey(object):
        def __init__(self, keyname):
            self.keyname = keyname

        def get_contents_as_string(self):
            return "test1\ntest2"

    fake_key = FakeKey('other.csv')

    class FakeBucket(object):
        vals = {'foobar.csv': fake_key}
        def get_key(self, keyname):
            return self.vals.get(keyname)

    fake_bucket = FakeBucket()
    get_bucket.return_value = fake_bucket

    @use_file('foobar.csv')
    def a_handle(keeper_file, *args, **options):
        lines = []
        for line in keeper_file:
            lines.append(line)
        return lines

    a_handle.when.called_with().should.return_value(["test1", "test2"])


@patch("keeper.core.get_bucket")
def test_result_csv(get_bucket):
    class FakeKey(object):
        def __init__(self, keyname):
            self.keyname = keyname

        def get_contents_as_string(self):
            return "test1,test2\nblue,green\n"

    fake_key = FakeKey('other.csv')

    class FakeBucket(object):
        vals = {'foobar.csv': fake_key}
        def get_key(self, keyname):
            return self.vals.get(keyname)

    fake_bucket = FakeBucket()
    get_bucket.return_value = fake_bucket

    @use_file('foobar.csv')
    def a_handle(keeper_file, *args, **options):
        lines = []
        for line in keeper_file.csv:
            lines.append(tuple(line))
        return lines

    a_handle.when.called_with().should.return_value([("test1", "test2"), ("blue", "green")])


@patch("keeper.core.get_bucket")
def test_result_json(get_bucket):
    class FakeKey(object):
        def __init__(self, keyname):
            self.keyname = keyname

        def get_contents_as_string(self):
            return '{"test1": "test2",\n"blue":{\n"a":"green"}}'

    fake_key = FakeKey('other.json')

    class FakeBucket(object):
        vals = {'foobar.json': fake_key}
        def get_key(self, keyname):
            return self.vals.get(keyname)

    fake_bucket = FakeBucket()
    get_bucket.return_value = fake_bucket

    @use_file('foobar.json')
    def a_handle(keeper_file, *args, **options):
        return keeper_file.json

    a_handle.when.called_with().should.return_value({
        'test1': 'test2',
        'blue': {
            'a': 'green'
        }
    })


@patch("keeper.core.get_bucket")
def test_key_doesnt_exist(get_bucket):
    get_bucket.return_value.get_key.return_value = None

    @use_file('foobar.csv')
    def a_handle(keeper_file, *args, **options):
        pass

    a_handle.when.called_with().should.throw(IOError,
        'The file foobar.csv cannot be found on S3.')


@patch("keeper.core.settings")
@patch("keeper.core.boto.connect_s3")
def test_get_bucket(connect_s3, settings):
    connect_s3.return_value.get_bucket.return_value = "foobar"
    get_bucket.when.called_with().should.return_value("foobar")


@patch('keeper.core.open', mock_open(read_data='local contents\nand some more'), create=True)
@patch("keeper.core.get_bucket")
def test_local_result(get_bucket):
    get_bucket.return_value.get_key.return_value = None

    @use_file('foobar.csv')
    def a_handle(keeper_file, *args, **options):
        lines = []
        for line in keeper_file:
            lines.append(line)
        return lines

    a_handle.when.called_with(local=True).should.return_value(['local contents', 'and some more'])
