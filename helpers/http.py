# -*- coding: utf-8 -*-
"""
helpers.http

Http request/response helper functions

* created: 2013-06-25 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-08-26 kchan
"""

import json


def json_response(response, data):
    """
    Utility function to return HTTP response as json data.

    :param response: HttpResponse or subclass
    :param data: dict to json serialize
    :returns: calls http response class to return data
    """
    return response(json.dumps(data), content_type='application/json')


def get_client_ip(request):
    """
    Get user's IP address.
    * from:
    http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
