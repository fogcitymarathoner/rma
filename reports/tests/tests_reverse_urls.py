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
        Reports - test the reverse urls for the exposed display pages
        """
        #
        # Parts Reports
        #
        url = reverse('report_parts')
        pattern = '^/crm_test/reports/parts/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('report_parts_all_time')
        pattern = '^/crm_test/reports/parts_all_time/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('report_parts_by_part_number')
        pattern = '^/crm_test/reports/parts_by_part_number/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        #
        url = reverse('report_parts_by_quarter_by_site')
        pattern = '^/crm_test/reports/report_parts_by_quarter_by_site/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        #
        url = reverse('report_parts_in_life')
        pattern = '^/crm_test/reports/report_parts_in_life/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        #
        url = reverse('report_parts_out_of_life')
        pattern = '^/crm_test/reports/report_parts_out_of_life/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        #
        url = reverse('report_unapproved_rmas')

        pattern = '^/crm_test/reports/report_unapproved_rmas/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
        #
        url = reverse('report_return_inventory')

        pattern = '^/crm_test/reports/report_return_inventory/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('report_customer_rma')
        pattern = '^/crm_test/reports/report_customer_rma/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('report_customer_sites')
        pattern = '^/crm_test/reports/report_customer_sites/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('report_user_roles')
        pattern = '^/crm_test/reports/report_user_roles/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('show_sites_rmas', args=(), kwargs={'id': 1})
        pattern = '^/crm_test/reports/show_sites_rmas/1$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('show_rma', args=(), kwargs={'id': 1})
        pattern = '^/crm_test/reports/show_rma/1$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('operation_not_allowed')
        pattern = '^/crm_test/reports/operation_not_allowed/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)