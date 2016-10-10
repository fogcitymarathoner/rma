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
            'xml_helpers',
            'xml_helpers.migrations',
            'xml_helpers.lib',
            'xml_helpers.management',
            'xml_helpers.management.commands',
            'xml_helpers.management.commands.build_mongo_extra_data_indices',
            'xml_helpers.management.commands.clear_redis_sessions',
            'xml_helpers.management.commands.read_all_commissioned_sites',
        ]
        for a in apps:
            self.assertTrue(module_exists(a))
