# -*- coding: utf-8 -*-
"""
helpers.tests.urlhelpers

Tests for helpers.urlhelpers module.

* created: 2013-09-01 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-27 kchan
"""

from django.core.urlresolvers import reverse

from helpers.test.base import SimpleTestCase
from helpers.test.utils import module_exists
from helpers.urlhelpers import (
    url_with_qs,
    login_url,
)


class UrlHelpersTests(SimpleTestCase):

    def test_module_imports(self):
        """
        Ensure modules are importable.
        """
        apps = [
            'helpers',
            'helpers.urlhelpers',
        ]
        for a in apps:
            self.assertTrue(module_exists(a))


    def test_url_with_qs_2(self):
        """
        Test url_with_qs function.
        """
        self._msg('test', 'test_url_with_qs_2', first=True)
        # test example url
        url = url_with_qs('/some-url/', a='b', c='d')
        result_url = '/some-url/?a=b&c=d'
        self.assertEqual(result_url, url)
        self._msg('test url', url)
