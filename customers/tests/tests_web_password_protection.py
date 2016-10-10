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

    def test_password_protection_on_commissioned_sites_list_page(self):
        """
        Ensure that commissioned sites list page is password protected
        """

        factory = RequestFactory()

        c0_url = reverse('list_customers')

        resp = self.app.get(c0_url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('view_customer', args=(), kwargs={'id': 22})

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('create_customer')

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)


        url = reverse('delete_customer', args=(), kwargs={'id': 22})

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
        url = reverse('edit_customer', args=(), kwargs={'id': 22})

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
