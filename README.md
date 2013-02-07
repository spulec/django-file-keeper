## Django-File-Keeper - file storage for management command in django

Do you ever commit large data fixtures to your git repo just so that you can run a once-off management command with that data? Not anymore.

Django-File-Keeper makes it easy to seamlessly have those files uploaded to S3 during development and downloaded from S3 on production meaning that you never need to commit those fixtures again.

For example, imagine the marketing department hands you a csv file of new users (new_users.csv) that need to be added into our system.

First, we upload the file to s3.

```bash
./manage.py upload_data_file new_users.csv
```

Make sure to double-check that the bucket you're using isn't world-readable.

Then we write our management command to add those users.

```python
from django.core.management.base import BaseCommand
from keeper import use_file

class Command(BaseCommand):

    @use_file('new_users.csv')
    def handle(self, keeper_file, *args, **options):
        for username, email in keeper_file.csv:
            User.objects.get_or_create(username, email)
```

That's it! When this runs on production, it will automatically grab the file from S3 and pass it into the management command as `keeper_file`.

# More Advanced

## CSV:

```python
from django.core.management.base import BaseCommand
from keeper import use_file

class Command(BaseCommand):

    @use_file('foobar.csv')
    def handle(self, keeper_file, *args, **options):
        for line in keeper_file.csv:
            print line
```

`keeper_file.csv` returns a python csv reader object.

## JSON:

```python
from django.core.management.base import BaseCommand
from keeper import use_file

class Command(BaseCommand):

    @use_file('foobar.csv')
    def handle(self, keeper_file, *args, **options):
        print keeper_file.json.keys()
```

`keeper_file.json` returns the json representation of the contents of the file.


# Installing

```bash
$ pip install django-file-keeper
```

In your django settings file, add the following variables so that file-keeper know which s3 bucket to use and what keys it should use to access it.

*   FILE_KEEPER_ACCESS_KEY
*   FILE_KEEPER_SECRET_KEY
*   FILE_KEEPER_BUCKET

