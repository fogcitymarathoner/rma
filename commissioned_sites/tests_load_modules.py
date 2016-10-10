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
        Ensure that commissioned site modules are importable.
        """
        apps = [
            'commissioned_sites',
            'commissioned_sites.admin',
            'commissioned_sites.forms',
            'commissioned_sites.migrations',
            'commissioned_sites.templatetags',
            'commissioned_sites.templatetags.clean_address',
            'commissioned_sites.templatetags.sharepoint_url',
            'commissioned_sites.models',
            'commissioned_sites.settings',
            'commissioned_sites.views',
        ]
        for a in apps:
            self.assertTrue(module_exists(a))
