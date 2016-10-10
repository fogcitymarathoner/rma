"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import re

from django.test import TestCase

from django.core.urlresolvers import reverse

class SimpleTest(TestCase):

    def test_reverse_urls(self):
        """
        Accounts - test the reverse urls for the exposed display pages
        """


        url = reverse('download_commissioned_site_attachment', args=(), kwargs={'id': 22})

        pattern = '/download-commissioned-site-attachment/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

