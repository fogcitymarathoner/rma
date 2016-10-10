__author__ = 'marc'

from django_webtest import WebTest

from django.test.client import RequestFactory

from django.core.urlresolvers import reverse

from django.contrib.auth.models import Group
import re
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

        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)


        url = reverse('view_rma', args=(), kwargs={'id': 22})

        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('download_rma_attachment', args=(), kwargs={'id': 22})


        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('rma_logout')


        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('rma_login')


        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)


        url = reverse('create_rma')
        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)



        url = reverse('approve_rma', args=(), kwargs={'id': 22})
        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
        url = reverse('edit_rma', args=(), kwargs={'id': 22})


        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
        url = reverse('delete_rma', args=(), kwargs={'id': 22})


        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
        url = reverse('manage_items', args=(), kwargs={'id': 22})


        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        url = reverse('manage_attachments', args=(), kwargs={'id': 22})


        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)


        url = reverse('manage_extra_fields', args=(), kwargs={'id': 22})


        resp = self.app.get(url).maybe_follow()
        self.assertEqual(resp.status_int, 200)

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)
