__author__ = 'marc'
# this breaks print
#from __future__ import print_function
import os
from django.conf import settings

XML_TEST_DATA_DIR = os.path.join(settings.BASE_DIR, 'test_data_rma')

from django.core.management.base import BaseCommand

from django.core.mail import send_mail
class Command(BaseCommand):
    args = ''
    help = ''
    def handle(self, *args, **options):


        send_mail('Subject here', 'Here is the message.', 'from@crm1.corp.enlightedinc.com',
            ['marc@rocketsredglare.com'], fail_silently=False)