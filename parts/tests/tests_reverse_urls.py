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
        Parts - test the reverse urls for the exposed display pages
        """
        url = reverse('list_parts')
        pattern = '^/crm_test/parts/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('view_part', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/parts/show/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('delete_part', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/parts/delete/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('delete_part_ops', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/parts/delete-ops/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('create_part')
        pattern = '/crm_test/parts/create/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('edit_part', args=(), kwargs={'id': 22})
        pattern = '/crm_test/parts/edit/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('edit_part_ops', args=(), kwargs={'id': 22})
        pattern = '/crm_test/parts/edit-ops/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)