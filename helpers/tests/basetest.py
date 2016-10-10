# -*- coding: utf-8 -*-
"""
helpers.tests.testbase

Tests for helpers.test module

* created: 2013-10-26 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-26 kchan
"""

from helpers.test.base import (
    SimpleTestCase,
    ProfileUserTestCase,
)
from helpers.test.utils import (
    module_exists,
    create_test_users,
)


class TestBaseTests(ProfileUserTestCase):

    def test_module_imports(self):
        """
        Ensure modules are importable.
        """
        apps = (
            'helpers.test',
            'helpers.test.base',
            'helpers.test.utils',
            'helpers.test.settings',
        )
        for a in apps:
            self.assertTrue(module_exists(a))

    def test_auth_user_test_case(self):
        """
        Ensure AuthUserTestCase is working correctly.
        """
        self._msg('test', 'test_auth_user_test_case', first=True)
        self.assertTrue(isinstance(self, TestBaseTests))
        self.assertTrue(hasattr(self, '_msg'))
        self.assertTrue(hasattr(self, '_login'))
        self.assertTrue(hasattr(self, '_logout'))
        self._msg('dir', dir(ProfileUserTestCase), linebreak=True)

    def test_module_exists(self):
        """
        Ensure module_exists function is working correctly.
        """
        self._msg('test', 'test_module_exists', first=True)
        modules = (
            'os',
            'os.path',
            're',
            'hashlib',
            'datetime',
            'logging',
            'pickle',
        )
        for m in modules:
            self.assertTrue(module_exists(m),
                msg="standard python module should be importable: %s" % m)
            self._msg('exists', m)
        nonexistent_modules = (
            'anonexistentmodule',
            'anotherbogusmod',
            'doesnotexist.one.two.three',
        )
        for m in nonexistent_modules:
            self.assertFalse(module_exists(m),
                msg="module should not be importable: %s" % m)
            self._msg('does not exist', m)

    def test_create_test_users(self):
        """
        Ensure create_test_users function is working correctly.
        """
        self._msg('test', 'test_create_test_users', first=True)
        start_num = len(self.users) + 1
        num_test_users = 3
        users = create_test_users(num_test_users, start_num=start_num)
        self.assertEqual(len(users), num_test_users)
        for u in users:
            self.assertTrue(u is not None)
            self.assertTrue(u.username is not None)
            self.assertTrue(u.password is not None)
            self.assertTrue(u.email is not None)
            self.assertTrue(u.user is not None)
            self.assertTrue(u.user.is_active)
            self._msg('user', 'id %d: %s (%s)' \
                % (int(u.user.id), u.user.get_username(), u.user.email))

    def test_user_info_set_status_status(self):
        """
        Ensure UserInfo class set_staff_status method is working correctly.
        """
        self._msg('test', 'test_user_info_set_staff_status', first=True)
        user = self.base_user.user
        self.assertTrue(user is not None)
        self._msg('user id', user.id)
        self._msg('username', user.get_username())
        self._msg('is_staff (before)', user.is_staff)
        self.base_user.set_staff_status(True)
        self.assertTrue(user.is_staff, msg="user should be staff")
        self._msg('is_staff (after)', user.is_staff)
