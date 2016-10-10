# -*- coding: utf-8 -*-
"""
helpers.files.tests

Tests for helpers.files

* created: 2013-10-26 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-27 kchan
"""

import os

from helpers.test.base import SimpleTestCase
from helpers.test.utils import module_exists

from .utils import (
    create_dir,
)


class FilesTests(SimpleTestCase):

    def test_module_imports(self):
        """
        Ensure modules are importable.
        """
        apps = (
            'helpers.files',
            'helpers.files.settings',
            'helpers.files.storage',
            'helpers.files.utils',
        )
        for a in apps:
            self.assertTrue(module_exists(a))

    def test_create_dir(self):
        """
        Ensure create_dir function is working correctly.
        """
        from helpers.media.utils import get_test_upload_dir
        self._msg('test', 'test_create_dir', first=True)
        path = os.path.join(get_test_upload_dir(), 'test-directory')
        result = create_dir(path)
        self.assertEqual(path, result)
        self.assertTrue(os.path.isdir(path))
        self._msg('test dir', path)
        os.rmdir(path)
