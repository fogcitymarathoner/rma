# -*- coding: utf-8 -*-
"""
helpers.profiles

Profiles utilities.
"""

from django.contrib.auth.models import User, AnonymousUser

from .settings import (
    DUMMY_USER_ID,
    DUMMY_USERNAME,
    DUMMY_EMAIL,
)


class DummyUser(AnonymousUser):
    """
    A mock/dummy user that functions as a placeholder stub.
    * used by the image upload processor (BaseUploadObject) as a
      stand-in for objects that do not have an authenticated user
      associated with them.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', DUMMY_USER_ID)
        self.username = kwargs.get('username', DUMMY_USERNAME)
        self.email = kwargs.get('email', DUMMY_EMAIL)
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')

    def __str__(self):
        return self.username


def get_user_by_id(user_id):
    """
    Get user from user_id
    """
    try:
        user = User.objects.get(pk=int(user_id))
    except (User.DoesNotExist, TypeError):
        user = None
    return user


def get_user(username):
    """
    Get user from username.
    """
    try:
        assert username
        user = User.objects.get(username__iexact=username)
    except (AssertionError, User.DoesNotExist):
        user = None
    return user


def get_user_by_email(email):
    """
    Get user from email address.
    """
    try:
        assert email
        user = User.objects.get(email__iexact=email)
    except (AssertionError, User.DoesNotExist):
        user = None
    return user
