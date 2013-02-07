## keeper - file storage for management command in django

```python
from django.core.management.base import BaseCommand
from keeper import use_file

class Command(BaseCommand):

    @use_file('foobar.txt')
    def handle(self, keeper_file, *args, **options):
        for line in keeper_file:
            print line
```

There is also a helper management command to upload files

```bash
./manage.py upload_data_file <filename>
```

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
$ [sudo] pip install django-file-keeper
```
