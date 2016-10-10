
import re

from django.test import TestCase
from parts.models import Part

class SimpleTest(TestCase):
    def test_models(self):
        """
        Parts - test that models save and retrieve data
        """
        new_part, created = Part.objects.get_or_create(description='new part')
        pattern = '^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'


        matched = re.search(pattern, new_part.last_modified_on.strftime('%Y-%d-%m'))
        self.assertTrue(matched)
        self.assertEqual('new part', new_part.description)