# -*- coding: utf-8 -*-
"""
helpers.views.mixins

Helper mixins for class-based views.

* created: 2013-09-06 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-09-27 kchan
"""

from helpers.http import json_response


class JsonResponseMixin(object):
    """
    Mixin with a ``json_response`` method.
    """

    def json_response(self, response, result):
        """
        Helper method to return a json response (for ajax posts).

        :param response: HttpResponse or variant
        :param result: dict of key-values to return to requester
        :returns: json response
        """
        return json_response(response, result)


class AuthMixin(object):
    """
    Mixin with an ``authenticated`` method.
    * this mixin verifies that the request user is authenticated.
    * set ``is_staff`` to True when calling the ``authenticated``
      method or use the ``user_is_staff`` method to verify user is
      logged-in staff.
    """

    authenticate_requests = True

    def authenticated(self, request, is_staff=False):
        """
        Helper method to verify user is authenticated.

        :returns: True if authenticated, else False
        """
        if not self.authenticate_requests and not is_staff:
            return True
        else:
            user = request.user
            if is_staff:
                authorized = user.is_staff
            else:
                authorized = True
            try:
                return user.is_authenticated() and user.is_active and authorized
            except AttributeError:
                return False

    def user_is_staff(self, request):
        """
        Verify user is staff.
        """
        return self.authenticated(request, is_staff=True)
