## keeper - file storage for management command in django

```python
from django.core.management.base import BaseCommand
from keeper import use_file

class Command(BaseCommand):

    @use_file('foobar.csv')
    def handle(self, file, *args, **options):
        for line in file:
            print line
```

There is also a helper management command to upload files

```bash
./manage.py upload_data_file <filename>
```

# Installing

```bash
$ [sudo] pip install django-file-keeper
```
