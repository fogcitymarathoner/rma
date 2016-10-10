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
from return_merchandise_authorizations.models import RmaAttachment
from django.core.files.uploadedfile import SimpleUploadedFile
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
        g = Group.objects.get(name='user')
        g.user_set.add(self.user)
        self.new_rma, created = Rma.objects.get_or_create(last_modified_by=self.user, customer=self.new_customer_site, date= '2014-04-04', case_number='1234' ,reference_number='1234', contact='bob')
        self.new_item, created = Item.objects.get_or_create(part=self.new_part, quantity=2, rma=self.new_rma)
        attachment = RmaAttachment.objects.get_or_create(rma=self.new_rma, file=SimpleUploadedFile('best_file_eva.txt', 'these are the file contents!'))
    def tearDown(self):
        pass

    def test_user_sees_customer_list(self):
        """
        Test that user can see customer list
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

        self.assertEqual(1, len(page.findAll(id='create-customer-button')))
    def test_user_create_customer(self):
        """
        Test that user can see customer create-customer form
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
    def test_user_view_customer_edit_delete_buttons(self):
        """
        Test that user view customer with edit and delete buttons
        """


        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        #<h1>Edit Customer Site</h1>
        url = reverse('view_customer', args=(), kwargs={'id': 1})
        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)

        self.assertEqual(1, len(page.findAll(id='edit-customer-button')))
        self.assertEqual(1, len(page.findAll(id='create-customer-button')))
        self.assertEqual(0, len(page.findAll(id='delete-customer-button')))


        title = page.findAll(id='view-customer-page')
        self.assertTrue(title[0].text, 'Customer')

    def test_user_view_customer_list(self):
        """
        Test that user view customer customer list
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


    def test_user_view_customer_site(self):
        """
        Test that user view customer site
        """
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()
        url = reverse('view_customer_site', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)

        title = page.findAll(id='view-customer-site-page')
        self.assertTrue(title[0].text, 'Customer Site With RMAs')


    def test_user_edit_customer(self):
        """
        Test that user can edit customer
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
        self.assertEqual(1, len(page.findAll(id='edit-customer-page')))


    def test_user_edit_customer_site(self):
        """
        Test that user can edit customer site
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
        self.assertEqual(1, len(page.findAll(id='edit-customer-site-page')))