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

import re
from return_merchandise_authorizations.acl import assign_user
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
        Test the manage RMA tabs, make sure the partial renders don't get unmapped
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

        # create new rma to navigate on


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

        url = reverse('approve_rma', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()

        form = resp.forms[0]
        resp = form.submit('Approve RMA').maybe_follow()

        url = reverse('view_rma', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()
        bs_doc = bs(resp.content)


        h3_list = bs_doc.findAll('h3')

        customer_data_count = 0
        for u in h3_list:
            if u.text == 'Customer Data':
                customer_data_count += 1
        self.assertEqual(1, customer_data_count)

        summary_data_count = 0
        for u in h3_list:
            if u.text == 'Summary of Issue':
                summary_data_count += 1
        self.assertEqual(1, summary_data_count)
        root_cause_count = 0
        for u in h3_list:
            if u.text == 'Root Cause Analysis':
                root_cause_count += 1
        self.assertEqual(1, root_cause_count)
        item_count = 0
        for u in h3_list:
            if u.text == 'Items':
                item_count += 1
        self.assertEqual(1, item_count)
        attachments_count = 0
        for u in h3_list:
            if u.text == 'Attachments':
                attachments_count += 1
        self.assertEqual(1, attachments_count)

        ##################
        url = reverse('manage_items', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()
        bs_doc = bs(resp.content)

        h3_list = bs_doc.findAll('h3')

        item_count = 0
        for u in h3_list:
            if u.text == 'Items':
                item_count += 1
        self.assertEqual(1, item_count)
        ##################

        url = reverse('manage_attachments', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()
        bs_doc = bs(resp.content)
        h3_list = bs_doc.findAll('h3')

        attachment_count = 0
        for u in h3_list:
            if u.text == 'Attachments':
                attachment_count += 1
        self.assertEqual(1, attachment_count)
        ##################

        url = reverse('manage_extra_fields', args=(), kwargs={'id': 1})

        resp = self.app.get(url).maybe_follow()
        bs_doc = bs(resp.content)

        h3_list = bs_doc.findAll('h3')

        extra_data_count = 0
        for u in h3_list:
            if u.text == 'Extra Data':
                extra_data_count += 1
        self.assertEqual(1, extra_data_count)
