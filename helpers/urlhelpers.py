# -*- coding: utf-8 -*-
"""
helpers.urlhelpers

URL helper functions.

* created: 2013-06-24 kevin chan <kefin@makedostudio.com>
* updated: 2013-08-26 kchan
"""

from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.http import urlencode

from garage import get_setting as _s


def url_with_qs(path, **kwargs):
    """
    Adds kwargs as query GET parameters to path.
    * from: http://www.mobile-web-consulting.de/post/3921808264/construct-url-with-query-parameters-in-django-with
    """
    return path + '?' + urlencode(kwargs)


def login_url(orig_url=None, redirect_back=True):
    """
    Utility function to return url to login form with 'next' query
    string set to 'orig_url'.

    :param orig_url: original url to use for "next" value in query string
    :param redirect_back: if True, set next to 'orig_url', else next=''
    :returns: login form url (with next in query string)
    """
    if orig_url is None or redirect_back is False:
        orig_url = ''
    url = _s('LOGIN_URL')
    if not url:
        try:
            url = reverse('auth_login')
        except NoReverseMatch:
            url = _s('DEFAULT_LOGIN_URL', '/')
    return url_with_qs(url, next=orig_url)


HomeURL = None

def get_home_url():
    """
    Get url for site home.
    """
    global HomeURL
    if HomeURL is None:
        url = _s('HOME_URL')
        if not url:
            try:
                url = reverse('home')
            except NoReverseMatch:
                url = '/'
        HomeURL = url
    return HomeURL
