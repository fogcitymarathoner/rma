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
        Services - test the reverse urls for the exposed display pages
        """

        url = reverse('numbered_returned_item_form', args=(), kwargs={'number': 22})

        pattern = '^/crm_test/services/numbered_return_item_form/22/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('customers_rmas_report', args=(), kwargs={'number': 22})

        pattern = '^/crm_test/services/customers_rmas_report/22/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('customers_sites_dropdown', args=(), kwargs={'number': 22})

        pattern = '^/crm_test/services/customers_sites_dropdown/22/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('returned_part_in_period_report', args=(), kwargs={'part_number': 22,
                                                                         'start_year': 2013,
                                                                         'start_month': 'jan',
                                                                         'start_day': '01',
                                                                         'end_year': 2014,
                                                                         'end_month': 'dec',
                                                                         'end_day': 31
                                                                         })

        pattern = '^/crm_test/services/returned_part_in_period_report/22/2013/jan/01/2014/dec/31/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)


        url = reverse('returned_part_all_time_report', args=(), kwargs={'part_number': 22 })

        pattern = '^/crm_test/services/returned_part_all_time_report/22/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('returned_part_by_part_number_report', args=(), kwargs={'part_number': 22 })

        pattern = '^/crm_test/services/returned_part_by_part_number_report/22/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)

        url = reverse('assign_role', args=(), kwargs={'id': 22, 'role': 'admin'})

        pattern = '^/crm_test/services/assign_role/22/admin/$'
        matched = re.search(pattern, url)
        self.assertTrue(matched)
