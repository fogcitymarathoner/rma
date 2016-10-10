__author__ = 'marc'

from django_webtest import WebTest
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from bs4 import BeautifulSoup as bs
from parts.models import Part
from customers.models import Customer
from django.core import mail
import re

from return_merchandise_authorizations.acl import assign_user
from customers.models import CustomerCompany
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

    def test_rma_email_sent(self):
        """
        Test RMA Create form with established customers check mail
        """

        new_customer, created = CustomerCompany.objects.get_or_create(company_name='new customer')
        new_customer_site, created = Customer.objects.get_or_create(name='new customer', customer=new_customer)

        new_part, created = Part.objects.get_or_create(description='new part')
        tst_user_username_good = 'tstuser_good'
        tst_user_pw_good = 'password_good'
        tst_user_email_good = 'email@email.com'

        user = User.objects.create_user(tst_user_username_good, tst_user_email_good, tst_user_pw_good)
        assign_user(user)

        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = tst_user_username_good
        form['password'] = tst_user_pw_good

        form.submit('submit').follow()

        url = reverse('create_rma')

        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)
        form = resp.forms["create-rma-with-an-existing-customer"]

        form['id_customer'] = new_customer.id

        form['part_0'].select(text="[description: new part, model_number:None, type: None, official_model_name: None]")
        form['quantity_0'] = 5
        form['date'] = '2014-11-30'
        form['case_number'] = '1234'
        form['reference_number'] = '1234'
        form['contact'] = 'bob'
        resp = form.submit('Save RMA').maybe_follow()

        self.assertEqual('RMA:new customer 1234', mail.outbox[0].subject)
        self.assertTrue(re.search('new customer', mail.outbox[0].body))
