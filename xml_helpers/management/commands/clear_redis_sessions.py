__author__ = 'marc'
# overnight routine to delete unused sessions


from django.core.management.base import BaseCommand
from xml_helpers.lib import remove_sessions_from_redis
class Command(BaseCommand):
    args = ''
    help = ''
    def handle(self, *args, **options):
        remove_sessions_from_redis()