__author__ = 'marc'

from django_webtest import WebTest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from bs4 import BeautifulSoup as bs
from parts.models import Part
from customers.models import Customer
from customers.models import CustomerCompany

from django.core import mail
import re
from return_merchandise_authorizations.models import Rma
from return_merchandise_authorizations.models import Item

from garage.logger import logger
class WebTest(WebTest):
    def setUp(self):
        g_admin = Group(name='admin')
        g_admin.save()
        g_approver = Group(name='approver')
        g_approver.save()
        g_poweruser = Group(name='poweruser')
        g_poweruser.save()
        g_user = Group(name='user')
        g_user.save()

        self.new_customer, created = CustomerCompany.objects.get_or_create(company_name='new customer')
        self.new_customer_site, created = Customer.objects.get_or_create(name='new customer', customer=self.new_customer)


        self.new_part, created = Part.objects.get_or_create(description='new part')
        self.tst_user_username_good = 'tstuser_good'
        self.tst_user_pw_good = 'password_good'
        self.tst_user_email_good = 'email@email.com'

        self.user = User.objects.create_user(self.tst_user_username_good, self.tst_user_email_good, self.tst_user_pw_good)

        self.new_rma, created = Rma.objects.get_or_create(last_modified_by=self.user, customer=self.new_customer_site, date= '2014-04-04', case_number='1234' ,reference_number='1234', contact='bob')
        self.new_item, created = Item.objects.get_or_create(part=self.new_part, quantity=2, rma=self.new_rma)


        self.tst_user_username_good = 'tstuser_admin_good'
        self.tst_user_pw_good = 'password_admin_good'
        self.tst_user_email_good = 'email@email_admin.com'
        self.user_admin = User.objects.create_user(self.tst_user_username_good, self.tst_user_email_good, self.tst_user_pw_good)
        self.user_admin.is_staff = True
        self.user_admin.is_superuser = True
        self.user_admin.save()

        g_admin.user_set.add(self.user_admin)
        g_approver.user_set.add(self.user_admin)
        g_poweruser.user_set.add(self.user_admin)
        g_user.user_set.add(self.user_admin)
        self.tst_user_username_good = 'tstuser_approver_good'
        self.tst_user_pw_good = 'password_approver_good'
        self.tst_user_email_good = 'email@email_approver.com'
        self.user_approver = User.objects.create_user(self.tst_user_username_good, self.tst_user_email_good, self.tst_user_pw_good)

        g_approver.user_set.add(self.user_approver)
        g_user.user_set.add(self.user_approver)


        self.tst_user_username_good = 'tstuser_poweruser_good'
        self.tst_user_pw_good = 'password_poweruser_good'
        self.tst_user_email_good = 'email@email_poweruser.com'
        self.user_poweruser = User.objects.create_user(self.tst_user_username_good, self.tst_user_email_good, self.tst_user_pw_good)

        g_approver.user_set.add(self.user_poweruser)
        g_poweruser.user_set.add(self.user_poweruser)
        g_user.user_set.add(self.user_poweruser)
        self.tst_user_username_good = 'tstuser_user_good'
        self.tst_user_pw_good = 'password_user_good'
        self.tst_user_email_good = 'email@email_user.com'
        self.user_user = User.objects.create_user(self.tst_user_username_good, self.tst_user_email_good, self.tst_user_pw_good)

        g_user.user_set.add(self.user_user)


        self.tst_user_username_good = 'tstuser_viewer_good'
        self.tst_user_pw_good = 'password_viewer_good'
        self.tst_user_email_good = 'email@email_viewer.com'
        self.user_user = User.objects.create_user(self.tst_user_username_good, self.tst_user_email_good, self.tst_user_pw_good)

    def tearDown(self):
        pass

    def test_viewer_report_user_roles_access(self):
        """
        Test that regular viewer can see report_user_roles
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('report_user_roles')

        resp = self.app.get(url)

        self.assertEqual(resp.status_int, 200)


        page = bs(resp.content)

        user_rows = page.findAll('tr', {'class': 'user-role-result'})
        self.assertEqual('tstuser_admin_good', user_rows[0].findAll('td')[0].text)
        self.assertEqual('admin', user_rows[0].findAll('td')[1].text)
        self.assertEqual('tstuser_approver_good', user_rows[1].findAll('td')[0].text)
        self.assertEqual('approver', user_rows[1].findAll('td')[1].text)
        self.assertEqual('tstuser_good', user_rows[2].findAll('td')[0].text)
        self.assertEqual('viewer', user_rows[2].findAll('td')[1].text)
        self.assertEqual('tstuser_poweruser_good', user_rows[3].findAll('td')[0].text)
        self.assertEqual('poweruser', user_rows[3].findAll('td')[1].text)
        self.assertEqual('tstuser_user_good', user_rows[4].findAll('td')[0].text)
        self.assertEqual('user', user_rows[4].findAll('td')[1].text)

        self.assertEqual('tstuser_viewer_good', user_rows[5].findAll('td')[0].text)
        self.assertEqual('viewer', user_rows[5].findAll('td')[1].text)