# -*- coding: utf-8 -*-
"""
helpers.test.utils

Utility functions for tests (using Django test runner).

* created: 2013-07-20 kevin chan <kefin@makedostudio.com>
* updated: 2013-11-21 kchan
"""

from django.contrib.auth.models import User

from garage.utils import safe_unicode
from garage import get_setting as _s
from helpers.test.settings import TEST_USER_TEMPLATE, DIVIDER
from helpers.txt.utils import uprint


# helper functions

def msg(label, txt, first=False, linebreak=False, divider=DIVIDER):
    """
    Print out debug message.
    """
    if first:
        uprint(u'\n%s' % safe_unicode(divider))
    label = safe_unicode(label)
    txt = safe_unicode(txt)
    if not linebreak:
        uprint(u'# %-16s : %s' % (label, txt))
    else:
        uprint(u'# %-16s :\n%s' % (label, txt))


def module_exists(module_name):
    """
    Check if module is importable.

    :param module_name: name of module to import (basestring)
    :returns: True if importable else False
    """
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True


class DummyObject(object):
    """
    Generic object for testing.
    """
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if not k.startswith('_'):
                setattr(self, k, v)


class UserInfo(object):
    """
    Simple object to store info for test user.
    """
    # verbose output
    verbosity = _s('TEST_VERBOSITY', 0)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.user = self.create_user()

    def _msg(self, *args, **kwargs):
        """
        Utility method to print out verbose test and debug messages.
        * print output only if verbosity level is above 2.
        """
        if self.verbosity > 2:
            msg(*args, **kwargs)

    def create_user(self):
        """
        Utility method to create user.
        """
        if self.username and self.password and self.email:
            user = User.objects.create_user(
                    self.username,
                    password=self.password,
                    email=self.email)
        else:
            user = None
        return user

    def set_staff_status(self, is_staff):
        """
        Change user ``is_staff`` status.

        :param is_staff: True or False
        :returns: user instance or None if user not found/some kind of error.
        """
        try:
            assert self.user and hasattr(self.user, 'is_staff')
        except AssertionError:
            pass
        else:
            self.user.is_staff = is_staff
            self.user.save()
        return self.user

    def print_user_info(self):
        """
        Utility method to print out user info.
        """
        if self.user:
            self._msg('username', self.username, first=True)
            self._msg('user id', str(self.user.id))
            self._msg('email', self.email)
        else:
            self._msg('user', 'None', first=True)


def create_test_users(num, start_num=1, user_template=None):
    """
    Create x number of test users.

    :param num: number of test users to create.
    :param start_num: starting num suffix for user
    :param user_template: tuple of (username_base, password_base, email_base)
    :returns: list of UserInfo objects.
    """
    start_num = int(start_num)
    username, password, email = user_template or TEST_USER_TEMPLATE
    return [
        UserInfo(username % str(n), password % str(n), email % str(n))
        for n in range(start_num, start_num + num)
    ]


### helper functions to verify and print form errors

def get_form_errors(form):
    """
    Return form.errors as a long string.

    :param form: form instance
    :returns: errors in a big string
    """
    return u'\n'.join([u'%s: %s' % (k, v) for k, v in form.errors.items()])


def get_field_error(form, field):
    """
    Utility function to retrieve the error message from form.errors.

    :param form: form instance
    :param field: field name
    :returns: error string or None
    """
    if field in form.errors:
        return form.errors[field]
    else:
        return None
