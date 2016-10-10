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
        Ensure modules are importable.
        """
        apps = [
            'return_merchandise_authorizations',
            'return_merchandise_authorizations.migrations',
            'return_merchandise_authorizations.templatetags',
            'return_merchandise_authorizations.templatetags.admin_url',
            'return_merchandise_authorizations.templatetags.phase',
            'return_merchandise_authorizations.templatetags.sharepoint_rma_url',
            'return_merchandise_authorizations.acl',
            'return_merchandise_authorizations.admin',
            'return_merchandise_authorizations.context_processors',
            'return_merchandise_authorizations.forms',
            'return_merchandise_authorizations.lib',
            'return_merchandise_authorizations.models',
            'return_merchandise_authorizations.settings',
            'return_merchandise_authorizations.urls',
            'return_merchandise_authorizations.views',
        ]
        for a in apps:
            self.assertTrue(module_exists(a))
