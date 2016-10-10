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

        c0_url = reverse('numbered_returned_item_form', args=(), kwargs={'number': 22})

        resp = self.app.get(c0_url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('returned_part_in_period_report', args=(), kwargs={'part_number': 22,
                                                                         'start_year': 2013,
                                                                         'start_month': 'jan',
                                                                         'start_day': '01',
                                                                         'end_year': 2014,
                                                                         'end_month': 'dec',
                                                                         'end_day': 31
                                                                         })

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('returned_part_all_time_report', args=(), kwargs={'part_number': 22})

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('returned_part_by_part_number_report', args=(), kwargs={'part_number': 22})

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
