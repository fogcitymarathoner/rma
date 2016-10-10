__author__ = 'marc'
# this breaks print
#from __future__ import print_function
import os
from django.conf import settings

XML_TEST_DATA_DIR = os.path.join(settings.BASE_DIR, 'test_data_commissioned_sites')

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from os import listdir
from os.path import isfile, join
from xml_helpers.lib import read_in_site_from_share_point_commissioned_site
class Command(BaseCommand):
    args = ''
    help = ''
    def handle(self, *args, **options):

        user = User.objects.get(username='crm')
        # empty customer database
        sites = Site.objects.all()
        for c in sites:
            c.delete()


        sharepoint_sites = [ f for f in listdir(XML_TEST_DATA_DIR) if isfile(join(XML_TEST_DATA_DIR,f)) ]
        for file in sharepoint_sites:
            abs_filename = os.path.join(XML_TEST_DATA_DIR, file)
            print 'Processing %s'%abs_filename
            read_in_site_from_share_point_commissioned_site(abs_filename, user)
