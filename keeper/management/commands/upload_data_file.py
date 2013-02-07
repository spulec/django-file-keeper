# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from optparse import make_option

import boto
from django.conf import settings
from django.core.management.base import BaseCommand

from keeper.core import set_key


class Command(BaseCommand):
    args = '<filename ...>'

    def handle(self, *args, **kwargs):
        for filename in args:
            set_key(filename)
