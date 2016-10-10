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
        url = reverse('home_page')

        pattern = '^/crm_test/rma/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('view_rma', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/rma/show/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('download_rma_attachment', args=(), kwargs={'id': 22})
        pattern = '/download-rma-attachment/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('rma_logout')
        pattern = '/crm_test/rma/logout/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('rma_login')
        pattern = '/crm_test/rma/login/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('create_rma')
        pattern = '/crm_test/rma/create/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        url = reverse('approve_rma', args=(), kwargs={'id': 22})
        pattern = '/crm_test/rma/approve/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        url = reverse('edit_rma', args=(), kwargs={'id': 22})
        pattern = '/crm_test/rma/edit/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        url = reverse('delete_rma', args=(), kwargs={'id': 22})

        pattern = '/crm_test/rma/delete/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        url = reverse('manage_items', args=(), kwargs={'id': 22})

        pattern = '/crm_test/rma/manage_items/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        url = reverse('manage_attachments', args=(), kwargs={'id': 22})

        pattern = '/crm_test/rma/manage_attachments/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('manage_extra_fields', args=(), kwargs={'id': 22})
        pattern = '/crm_test/rma/manage_extra_fields/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)




        url = reverse('download_rma_attachment', args=(), kwargs={'id': 22})

        pattern = '/crm_test/rma/crm_test/download-rma-attachment/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)