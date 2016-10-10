
import re

from django.test import TestCase
from customers.models import Customer
from customers.models import CustomerCompany

class SimpleTest(TestCase):
    def test_models(self):
        """
        Customers - test that models save and retrieve data
        """
        new_customer, created = CustomerCompany.objects.get_or_create(company_name='new customer')
        new_customer_site, created = Customer.objects.get_or_create(name='new customer', customer=new_customer)
        pattern = '^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'

        matched = re.search(pattern, new_customer_site.last_modified_on.strftime('%Y-%d-%m'))
        self.assertTrue(matched)
        self.assertEqual('new customer', new_customer_site.name)