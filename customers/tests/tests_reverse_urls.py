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
        Customers - test the reverse urls for the exposed display pages
        """
        url = reverse('list_customers')
        pattern = '^/crm_test/customers/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('create_customer')
        pattern = '^/crm_test/customers/create/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('view_customer', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/customers/show/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        url = reverse('delete_customer', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/customers/delete/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('edit_customer', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/customers/edit/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('list_customer_sites')
        pattern = '^/crm_test/customers/sites/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('view_customer_site', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/customers/show_site/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('create_customer_site')
        pattern = '^/crm_test/customers/create_site/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('create_customer_site_for_customer', args=(), kwargs={'customer_id': 22})

        pattern = '^/crm_test/customers/create_site_for_customer/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('delete_customer_site', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/customers/delete_site/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('delete_customer', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/customers/delete/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('edit_customer_site', args=(), kwargs={'id': 22})

        pattern = '^/crm_test/customers/edit_site/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
