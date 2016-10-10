# -*- coding: utf-8 -*-
"""
helpers.decorators

Utility decorators

* created: 2013-06-29 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-08-26 kchan
"""

from functools import wraps

from django.http import HttpResponseRedirect, Http404

from helpers.urlhelpers import login_url


### helper functions

def authenticated_only(func):
    """
    Decorator to check that user is logged in.
    * redirects request to login form if user is not authenticated.
    """
    def wrapped(request, *args, **kwargs):
        try:
            user = request.user
            assert user.is_active and user.is_authenticated()
            return func(request, *args, **kwargs)
        except (AssertionError, AttributeError):
            url = request.get_full_path()
            return HttpResponseRedirect(
                login_url(orig_url=url, redirect_back=True)
            )
    wrapped.__doc__ = func.__doc__
    wrapped.__name__ = func.__name__
    return wrapped


def staff_only(func):
    """
    Decorator to check that user is authenticated and staff
    * redirects request to login form if user is not authenticated;
    * raises 404 NOT FOUND error if user is authenticated but not
      staff.
    """
    def wrapped(request, *args, **kwargs):
        try:
            user = request.user
            assert user.is_active and user.is_authenticated()
        except (AssertionError, AttributeError):
            url = request.get_full_path()
            return HttpResponseRedirect(
                login_url(orig_url=url, redirect_back=True)
            )
        else:
            if not user.is_staff:
                raise Http404
            return func(request, *args, **kwargs)
    wrapped.__doc__ = func.__doc__
    wrapped.__name__ = func.__name__
    return wrapped
