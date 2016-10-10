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
        url = reverse('list_returned_items')

        pattern = '^/crm_test/returned_items/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('move_returned_items')
        pattern = '^/crm_test/returned_items/move_items'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('confirm_move_items')

        pattern = '^/crm_test/returned_items/move_items_confirm'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('create_returned_item', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/returned_items/create/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('edit_returned_item', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/returned_items/edit/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('delete_returned_item', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/returned_items/delete/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
