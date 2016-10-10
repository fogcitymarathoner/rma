__author__ = 'marc'

from django_webtest import WebTest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from bs4 import BeautifulSoup as bs
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

    def test_login(self):
        """
        Ensure that returned merchandise list page can be loggedin to
        """
        tst_user_username_bad = 'tstuser'
        tst_user_pw_bad = 'password'
        factory = RequestFactory()

        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = tst_user_username_bad
        form['password'] = tst_user_pw_bad

        resp = form.submit('submit').follow()

        pattern = '<h1>Please Log In</h1>'
        matched = re.search(pattern, resp.content)
        self.assertTrue(matched)

        tst_user_username_good = 'tstuser_good'
        tst_user_pw_good = 'password_good'
        tst_user_email_good = 'email@email.com'

        User.objects.create_user(tst_user_username_good, tst_user_email_good, tst_user_pw_good)

        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = tst_user_username_good
        form['password'] = tst_user_pw_good

        resp = form.submit('submit').follow()
        page = bs(resp.content)
        welcome_count = 0
        for s in page.findAll('span'):
            if s.has_attr('class'):
                if s['class'][0] == 'welcome-name':
                    welcome_count += 1
                    break
        self.assertEqual(1, welcome_count)
