# -*- coding: utf-8 -*-
"""
helpers.tests.http

Tests for helpers.http module.

* created: 2013-09-01 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-27 kchan
"""
import re
import json

from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseBadRequest,
    Http404
)

from helpers.test.base import SimpleTestCase
from helpers.test.utils import module_exists
from helpers.http import (
    json_response,
    get_client_ip,
)


class HttpTests(SimpleTestCase):

    def _verify_json_response(self, response, data, status_code):
        resp = json_response(response, data)
        json_str = resp.content
        resp_data = json.loads(json_str)
        self.assertEqual(resp.status_code, status_code)
        self._msg('test', status_code)
        self._msg('status', resp.status_code)
        self._msg('response content', json_str)
        for k, v in resp_data.items():
            self.assertEqual(data.get(k), v)
            self._msg('data[%s]' % k, v)

    def test_module_imports(self):
        """
        Ensure modules are importable.
        """
        apps = [
            'helpers',
            'helpers.http',
        ]
        for a in apps:
            self.assertTrue(module_exists(a))

    def test_json_response(self):
        """
        Test json_response function.
        """
        self._msg('test', 'json_response', first=True)
        test_msg = u'This is a test message'

        # test 200
        response = HttpResponse
        status_code = 200
        data = {
            'result': status_code,
            'content': test_msg,
        }
        self._verify_json_response(response, data, status_code)

        # test 400
        response = HttpResponseBadRequest
        status_code = 400
        data = {
            'result': status_code,
            'content': test_msg,
        }
        self._verify_json_response(response, data, status_code)

        # test 403
        response = HttpResponseForbidden
        status_code = 403
        data = {
            'result': status_code,
            'content': test_msg,
        }
        self._verify_json_response(response, data, status_code)

    def test_get_client_ip(self):
        """
        Test get_client_ip function.
        """
        factory = RequestFactory()
        """
        url = reverse('home')
        fake_remote_addr = '1.2.3.4'
        request = factory.get(url, REMOTE_ADDR=fake_remote_addr)
        ip = get_client_ip(request)
        self._msg('test', 'get_client_ip', first=True)
        self._msg('fake remote ip', fake_remote_addr)
        self.assertEqual(ip, fake_remote_addr)
        self._msg('ip', ip)
        """