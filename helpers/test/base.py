# -*- coding: utf-8 -*-
"""
helpers.test.base

Test classes based on Django TestCase

* created: 2013-07-21 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-27 kchan
"""

from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory

from garage import get_setting as _s
from helpers.test.utils import (
    msg,
    create_test_users,
    get_field_error,
)


VERBOSITY = _s('TEST_VERBOSITY', 0)


class SimpleTestCase(unittest.TestCase):
    """
    Test case based on Python unittest TestCase.
    """
    # verbose output
    verbosity = VERBOSITY

    def _msg(self, *args, **kwargs):
        """
        Utility method to print out verbose test and debug messages.
        * print output only if verbosity level is above 2.
        """
        if self.verbosity > 2:
            msg(*args, **kwargs)


# number of users to create for tests
NUM_TEST_USERS = 1

class ProfileUserTestCase(TestCase):
    """
    Test case with utility methods for logging in users and testing
    content for authenticated users.
    """
    # verbose output
    verbosity = VERBOSITY

    def _msg(self, *args, **kwargs):
        """
        Utility method to print out verbose test and debug messages.
        * print output only if verbosity level is above 2.
        """
        if self.verbosity > 2:
            msg(*args, **kwargs)

    def setUp(self, num_test_users=NUM_TEST_USERS):
        """
        Do setup for tests.
        """
        if hasattr(self, 'client') and self.client:
            self.c = self.client
        else:
            self.c = Client()
        self.users = create_test_users(num_test_users)
        self.base_user = self.users[0]
        self.factory = RequestFactory()

    def _login(self, username=None, password=None):
        """
        Log in test user using Django auth login().
        """
        if not username:
            username = self.base_user.username
        if not password:
            password = self.base_user.password
        return self.c.login(username=username, password=password)

    def _logout(self):
        """
        Log out user.
        """
        self.c.logout()

    def _verify_form_errors(self, form, fields, error=True, print_msg=False):
        """
        Utility method to verify form field errors.

        :param form: form instance
        :param fields: list of fields to verify
        :param error: assert error if True, assert no error if False
        :param print_msg: print form error message if assertion fails
        """
        started = False
        for field in fields:
            e = get_field_error(form, field)
            if error:
                if not e and print_msg:
                    if not started:
                        print u''
                        started = True
                    self._msg('%s error' % field, e)
                self.assertTrue(e is not None)
            else:
                if e and print_msg:
                    if not started:
                        print u''
                        started = True
                    self._msg('%s error' % field, e)
                self.assertTrue(e is None)
