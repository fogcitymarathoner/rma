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
        url = reverse('commissioned_sites')
        pattern = '^/crm_test/commissioned-sites'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('view_site', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/commissioned-sites/show/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)