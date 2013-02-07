import csv
import functools
import json
from StringIO import StringIO

import boto
from django.conf import settings


class KeeperResult(object):
    def __init__(self, contents):
        self.contents = contents

    def __iter__(self):
        for line in self.contents.split('\n'):
            yield line

    def __unicode__(self):
        result_string = u"KeeperResult: {}"
        if len(self.contents) > 50:
            result_string = u"KeeperResult: {}..."

        return result_string.format(self.contents[:50])

    @property
    def csv(self):
        csv_reader = csv.reader(StringIO(self.contents))
        return csv_reader

    @property
    def json(self):
        return json.loads(self.contents)


class Keeper(object):
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, func):
        return self.decorate_callable(func)

    def decorate_callable(self, func):
        def wrapper(*args, **kwargs):
            local = kwargs.get('local')
            if local:
                # If local setting on, just read the file
                file_contents = open(self.filename).read()
            else:
                file_contents = self.get_file()
            keeper_file = KeeperResult(file_contents)
            # TODO do we need to do keeper_file=?
            result = func(keeper_file=keeper_file, *args, **kwargs)
            return result
        functools.update_wrapper(wrapper, func)
        return wrapper

    def get_file(self):
        bucket = get_bucket()
        key = bucket.get_key(self.filename)
        if key is None:
            raise IOError(
                'The file {} cannot be found on S3.'.format(self.filename))

        return key.get_contents_as_string()


def use_file(filename):
    return Keeper(filename)


def get_bucket():
    conn = boto.connect_s3(settings.FILE_KEEPER_ACCESS_KEY,
                    settings.FILE_KEEPER_SECRET_KEY)
    bucket = conn.get_bucket(settings.FILE_KEEPER_BUCKET)
    return bucket


def get_input(prompt):
    return raw_input(prompt)

def set_key(filename):
    bucket = get_bucket()
    key = bucket.get_key(filename)
    if key is not None:
        prompt = "The file {} already exists on S3. Would you like to overwrite it[Y/N]".format(filename)
        response = get_input(prompt)
        if response != "Y":
            print("Not overwriting {}".format(filename))
            return

    key = bucket.new_key(filename)
    key.set_contents_from_filename(filename)
