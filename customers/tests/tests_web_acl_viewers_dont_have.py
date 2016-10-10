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

    def test_no_customer_create_button(self):
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
        page = bs(resp.content)

        self.assertEqual(0, len(page.findAll(id='create-customer-button')))

        title = page.findAll(id='page-title')
        self.assertTrue(title[0].text, 'Customers')
    def test_no_customer_site_create_button(self):
        """
        Test that regular viewer cannot see create-customer-button
        """
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('list_customer_sites')

        resp = self.app.get(url).maybe_follow()
        page = bs(resp.content)

        self.assertEqual(0, len(page.findAll(id='create-customer-site-button')))

        title = page.findAll(id='page-title')
        self.assertTrue(title[0].text, 'Customer Sites')
    def test_viewer_cannot_edit_or_delete_customer(self):
        """
        Test that regular viewer can see a customer, but not edit or delete
        """
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()


        url = reverse('view_customer', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)

        self.assertEqual(0, len(page.findAll(id='edit-customer-button')))
        self.assertEqual(0, len(page.findAll(id='delete-customer-button')))


        title = page.findAll(id='view-customer-page')
        self.assertTrue(title[0].text, 'Customer')


    def test_no_customer_site_create_button(self):
        """
        Test that elements exposed to user are masked from view
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('list_customer_sites')

        resp = self.app.get(url).maybe_follow()
        page = bs(resp.content)

        title = page.findAll(id='page-title')
        self.assertTrue(title[0].text, 'Customer Sites')

        self.assertEqual(0, len(page.findAll(id='edit-customer-site-button')))
        self.assertEqual(0, len(page.findAll(id='delete-customer-site-button')))
    def test_viewer_creating_customer_site_redirected(self):
        """
        Test that if a user types in create site url he is redirected to error page
        """
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('create_customer_site')
        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)

        self.assertEqual(1, len(page.findAll(id='inadequate-privileges-warning')))

    def test_viewer_creating_customer_redirected(self):
        """
        Test that if a user types in create customer url he is redirected to error page
        """

        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('create_customer')
        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)
        self.assertEqual(1, len(page.findAll(id='inadequate-privileges-warning')))


    def test_viewer_deleting_customer_redirected(self):
        """
        Test that if a viewer types in delete customer url is redirected to error page
        """
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('delete_customer', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()


        page = bs(resp.content)

        self.assertEqual(1, len(page.findAll(id='inadequate-privileges-warning')))
    def test_viewer_deleting_customer_site_redirected(self):
        """
        Test that if a viewer types in delete customer site url is redirected to error page
        """
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('delete_customer_site', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()


        page = bs(resp.content)

        self.assertEqual(1, len(page.findAll(id='inadequate-privileges-warning')))

    def test_viewer_edit_customer_redirected(self):
        """
        Test that viewer typing in edit customer is redirected to error page
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('edit_customer', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()


        page = bs(resp.content)


        self.assertEqual(1, len(page.findAll(id='inadequate-privileges-warning')))
    def test_viewer_edit_customer_site_redirected(self):
        """
        Test that viewer typing in edit customer site is redirected to error page
        """
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('edit_customer_site', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()


        page = bs(resp.content)
        self.assertEqual(1, len(page.findAll(id='inadequate-privileges-warning')))