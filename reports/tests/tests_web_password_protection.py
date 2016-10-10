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
        Ensure that reports list page is password protected
        """

        factory = RequestFactory()

        url = reverse('report_parts')

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('report_parts_all_time')

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
        url = reverse('report_parts_by_part_number')

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
        url = reverse('report_parts_by_quarter_by_site')

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
        url = reverse('report_parts_in_life')

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
        url = reverse('report_parts_out_of_life')

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)


        url = reverse('report_unapproved_rmas')

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('report_return_inventory')


        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)


        url = reverse('report_customer_rma')
        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('report_customer_sites')
        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('report_user_roles')
        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)


        url = reverse('show_sites_rmas', args=(), kwargs={'id': 22})
        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('show_rma', args=(), kwargs={'id': 22})
        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)