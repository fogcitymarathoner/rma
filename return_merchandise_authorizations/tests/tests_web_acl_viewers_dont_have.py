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
from return_merchandise_authorizations.models import Item

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

    def test_user_masks(self):
        """
        Test that elements exposed to user are masked from view
        """

        new_customer, created = CustomerCompany.objects.get_or_create(company_name='new customer')
        new_customer_site, created = Customer.objects.get_or_create(name='new customer', customer=new_customer)

        new_part, created = Part.objects.get_or_create(description='new part')
        tst_user_username_good = 'tstuser_good'
        tst_user_pw_good = 'password_good'
        tst_user_email_good = 'email@email.com'

        user = User.objects.create_user(tst_user_username_good, tst_user_email_good, tst_user_pw_good)

        new_rma, created = Rma.objects.get_or_create(last_modified_by=user, customer=new_customer_site, date= '2014-04-04', case_number='1234' ,reference_number='1234', contact='bob')
        new_item, created = Item.objects.get_or_create(part=new_part, quantity=2, rma=new_rma)
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = tst_user_username_good
        form['password'] = tst_user_pw_good

        resp = form.submit('submit').follow()

        page = bs(resp.content)

        self.assertEqual(0, len(page.findAll(id='create-rma-button')))



        url = reverse('view_rma', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()


        page = bs(resp.content)

        self.assertEqual(0, len(page.findAll(id='edit-rma-button')))
        self.assertEqual(0, len(page.findAll(id='approve-rma-button')))
        self.assertEqual(0, len(page.findAll(id='delete-rma-button')))


        url = reverse('manage_items', args=(), kwargs={'id': 1})
        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)
        self.assertEqual(0, len(page.findAll(id='create-returned-item-button')))
        self.assertEqual(0, len(page.findAll(attrs={'class':'manage-returned-item-operations'})))



        url = reverse('manage_attachments', args=(), kwargs={'id': 1})
        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)
        self.assertEqual(0, len(page.findAll(id='create-rma-attachment-button')))
        self.assertEqual(0, len(page.findAll(id='delete-rma-attachment-button')))


        page = bs(resp.content)
        url = reverse('manage_extra_fields', args=(), kwargs={'id': 1})
        resp = self.app.get(url).maybe_follow()


        page = bs(resp.content)

        self.assertEqual(0, len(page.findAll(id='save-extra-data')))

        self.assertEqual(0, len(page.findAll('input', attrs={'class':'extra-data-input'})))