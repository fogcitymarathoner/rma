__author__ = 'marc'

from django_webtest import WebTest

from django.test.client import RequestFactory

from django.core.urlresolvers import reverse
import re

from django.contrib.auth.models import Group
class WebTest(WebTest):

    def setUp(self):
        g = Group(name='admin')
        g.save()
        g = Group(name='approver')
        g.save()
        g = Group(name='poweruser')
        g.save()
        g = Group(name='user')
        g.save()
    def tearDown(self):
        pass

    def test_password_protection_on_rma_pages(self):
        """
        Ensure that returned merchandise list page is password protected
        """

        factory = RequestFactory()

        c0_url = reverse('move_parts')

        resp = self.app.get(c0_url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        c0_url = reverse('admin_rma_extra_fields')

        resp = self.app.get(c0_url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)



        url = reverse('view_part_to_move', args=(), kwargs={'id': 22})

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
