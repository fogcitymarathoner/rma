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
        url = reverse('move_parts')

        pattern = '^/crm_test/operations/move_parts/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('admin_rma_extra_fields')

        pattern = '^/crm_test/operations/admin_rma_extra_fields/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)



        url = reverse('view_part_to_move', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/operations/show_part_to_move/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('view_customer_site_to_reassign', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/operations/view_customer_site_to_reassign/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('assign_customer_to_site_new_customer', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/operations/assign_customer_to_site_new_customer/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('operations_edit_customer_site', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/operations/edit_customer_site/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('assign_customer_select_customer', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/operations/assign_customer_select_customer/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('reassign_customers_to_customer_sites')
        pattern = '^/crm_test/operations/reassign_customers_to_customer_sites/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('manage_users_roles')
        pattern = '^/crm_test/operations/manage_users_roles/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('manage_user_roles', args=(), kwargs={'id': 22})
        pattern = '^/crm_test/operations/manage_user_roles/22$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)