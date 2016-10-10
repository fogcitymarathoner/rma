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
from bs4 import BeautifulSoup as bs
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
        self.new_part2, created = Part.objects.get_or_create(description='new part2')
        self.tst_user_username_good = 'tstuser_good'
        self.tst_user_pw_good = 'password_good'
        self.tst_user_email_good = 'email@email.com'

        self.user = User.objects.create_user(self.tst_user_username_good, self.tst_user_email_good, self.tst_user_pw_good)

        g = Group.objects.get(name='user')
        g.user_set.add(self.user)
        self.new_rma, created = Rma.objects.get_or_create(last_modified_by=self.user, customer=self.new_customer_site, date= '2014-04-04', case_number='1234' ,reference_number='1234', contact='bob')
        self.new_item, created = Item.objects.get_or_create(part=self.new_part, quantity=2, rma=self.new_rma)
        self.attachment = RmaAttachment.objects.get_or_create(rma=self.new_rma, file=SimpleUploadedFile('best_file_eva.txt', 'these are the file contents!'))
    def tearDown(self):
        pass


    def test_user_can_create_returned_items(self):
        """
        Test that user can create items
        """
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('create_returned_item', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)
        self.assertEqual(0, len(page.findAll(id='inadequate-privileges-warning')))

        form =  resp.forms['create-returned-item']

        form['part'].select(text="[description: new part, model_number:None, type: None, official_model_name: None]")
        form['quantity'] = '5'
        form['note'] = 'hi im a note!'

        resp = form.submit('Save Returned Part').maybe_follow()
        page = bs(resp.content)
        self.assertEqual('Manage Return Merchandise Authorization for', page.findAll('h1')[0].text)

    def test_user_can_create_submit_returned_items_form_with_error(self):
        """
        Test that dirty data in Item form bounced user back to form
        """
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = self.tst_user_username_good
        form['password'] = self.tst_user_pw_good

        resp = form.submit('submit').follow()

        url = reverse('create_returned_item', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()

        page = bs(resp.content)
        self.assertEqual(0, len(page.findAll(id='inadequate-privileges-warning')))

        form =  resp.forms['create-returned-item']

        form['part'].select(text="[description: new part, model_number:None, type: None, official_model_name: None]")
        form['note'] = 'hi im a note!'

        resp = form.submit('Save Returned Part').maybe_follow()
        page = bs(resp.content)
        self.assertEqual(1, len(page.findAll('ul', {'class':'errorlist'})))
