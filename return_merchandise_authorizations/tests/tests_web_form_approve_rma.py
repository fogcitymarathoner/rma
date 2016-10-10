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
from return_merchandise_authorizations.models import Rma

from return_merchandise_authorizations.acl import assign_approver
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

    def test_create_form(self):
        """
        Test RMA approval
        """


        new_customer, created = CustomerCompany.objects.get_or_create(company_name='new customer')
        new_customer_site, created = Customer.objects.get_or_create(name='new customer', customer=new_customer)


        new_part, created = Part.objects.get_or_create(description='new part')
        tst_user_username_good = 'tstuser_good'
        tst_user_pw_good = 'password_good'
        tst_user_email_good = 'email@email.com'

        user = User.objects.create_user(tst_user_username_good, tst_user_email_good, tst_user_pw_good)
        assign_approver(user)
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = tst_user_username_good
        form['password'] = tst_user_pw_good

        form.submit('submit').follow()


        new_rma, created = Rma.objects.get_or_create(id=99999, last_modified_by=user, customer=new_customer_site, date= '2014-04-04', case_number='1234' ,reference_number='1234', contact='bob')

        url = reverse('approve_rma', args=(), kwargs={'id': 99999})

        resp = self.app.get(url).maybe_follow()

        form = resp.forms[0]
        resp = form.submit('Approve RMA').maybe_follow()
        rma = Rma.objects.get(pk=99999)
        self.assertEqual(2, rma.approved)

        self.assertEqual('RMA:new customer 1234 APPROVED', mail.outbox[0].subject)

        self.assertTrue(re.search('new customer', mail.outbox[0].body))