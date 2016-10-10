__author__ = 'marc'

from django.core.management.base import BaseCommand

import redis
import json
from django.conf import settings

from pymongo import MongoClient

class Command(BaseCommand):
    args = ''
    help = ''
    def handle(self, *args, **options):
        r = redis.StrictRedis(host='localhost', port=6379, db=settings.SESSION_REDIS_DB)

        rfields = json.loads(r.get(settings.SUB_URL.replace('/','')+':rma_extra_data'))

        client = MongoClient()
        db = client[settings.MONGO_DB]
        extra_data = db.extra_data
        for field in rfields:
            extra_data.create_index(field)