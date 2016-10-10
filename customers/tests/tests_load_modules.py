__author__ = 'marc'
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


from helpers.test.utils import module_exists
class SimpleTest(TestCase):

    def test_module_imports(self):
        """
        Ensure Customers modules are importable.
        """
        apps = [
            'customers',
            'customers.migrations',
            'customers.management',
            'customers.management.commands',
            'customers.management.commands.load_customers_to_redis',
            'customers.forms',
            'customers.admin',
            'customers.models',
            'customers.urls',
            'customers.views',
        ]
        for a in apps:
            self.assertTrue(module_exists(a))
