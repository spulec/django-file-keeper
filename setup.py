#!/usr/bin/env python

import sys
from setuptools import setup, find_packages

setup(
    name='django-file-keeper',
    version='0.0.1',
    description='file storage for management command in django',
    author='Steve Pulec',
    author_email='spulec@gmail',
    url='https://github.com/spulec/django-file-keeper',
    packages=find_packages(),
    include_package_data=True,
)
