__author__ = 'marc'
from django.core.management.base import BaseCommand

from customers.models import Customer
from return_merchandise_authorizations.models import Rma
from django.conf import settings
from django.core.urlresolvers import reverse
"""
Load cache.xml to redis database
"""

from xml_helpers.lib import load_customers_to_redis

class Command(BaseCommand):
    args = ''
    help = ''
    def handle(self, *args, **options):
        load_customers_to_redis()
