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

        self.new_customer, created = CustomerCompany.objects.get_or_create(company_name='new customer')
        self.new_customer_site, created = Customer.objects.get_or_create(name='new customer', customer=self.new_customer)


        self.new_part, created = Part.objects.get_or_create(description='new part')
        self.tst_user_username_good = 'tstuser_good'
        self.tst_user_pw_good = 'password_good'
        self.tst_user_email_good = 'email@email.com'

        self.user = User.objects.create_user(self.tst_user_username_good, self.tst_user_email_good, self.tst_user_pw_good)

        self.new_rma, created = Rma.objects.get_or_create(last_modified_by=self.user, customer=self.new_customer_site, date= '2014-04-04', case_number='1234' ,reference_number='1234', contact='bob')
        self.new_item, created = Item.objects.get_or_create(part=self.new_part, quantity=2, rma=self.new_rma)

    def tearDown(self):
        pass

    def test_viewer_report_parts_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('list_customers')

        resp = self.app.get(url).maybe_follow()

        url = reverse('report_parts')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_report_parts_all_time_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('report_parts_all_time')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_report_parts_by_part_number_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('report_parts_by_part_number')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_report_parts_by_quarter_by_site_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('report_parts_by_quarter_by_site')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_report_parts_in_life_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('report_parts_in_life')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_report_parts_out_of_life_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('report_parts_out_of_life')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_report_unapproved_rmas_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('report_unapproved_rmas')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_report_return_inventory_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('report_return_inventory')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_report_customer_rma_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('report_customer_rma')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_report_customer_sites_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('report_customer_sites')

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
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


    def test_viewer_show_sites_rmas_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('show_sites_rmas', args=(), kwargs={'id': 1})

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)
    def test_viewer_show_rma_access(self):
        """
        Test that regular viewer cannot see create-customer-button
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('show_rma', args=(), kwargs={'id': 1})

        resp = self.app.get(url)
        self.assertEqual(resp.status_int, 200)