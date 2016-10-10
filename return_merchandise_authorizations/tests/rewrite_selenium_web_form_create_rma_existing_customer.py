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
    """
    create an RMA from selecting customer/site combination from list
    """
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
        Test RMA Create form with established customers
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
        resp = form.submit('Save RMA').maybe_follow()
        bs_doc = bs(resp.content)
        # with no inputs make sure you get 4 messages
        # no site selected
        # no case number
        # no reference number
        # no contact
        # * no parts selected - not in error list
        self.assertEqual('Please correct errors belowYOU MUST SELECT SOME ITEMS', bs_doc.p.get_text())
        ul_list = bs_doc.findAll('ul')
        error_count = 0
        for u in ul_list:
            if u.has_attr('class'):
                if u['class'][0] == 'errorlist':
                    error_count += 1
        self.assertEqual(4, error_count)
        # after selecting a customer make sure you get at least 4 errorlist class messages
        form = resp.forms["create-rma-with-an-existing-customer"]

        form['id_customer'] = new_customer.id

        resp = form.submit('Save RMA').maybe_follow()
        bs_doc = bs(resp.content)

        ul_list = bs_doc.findAll('ul')
        error_count = 0
        for u in ul_list:
            if u.has_attr('class'):
                if u['class'][0] == 'errorlist':
                    error_count += 1
        # after selecting a site you get 4 messages
        # no case number
        # no reference number
        # no contact
        # * no parts selected - not in error list
        self.assertEqual(3, error_count)

        # select a part without a quantity
        form = resp.forms["create-rma-with-an-existing-customer"]
        form['part_0'].select(text="[description: new part, model_number:None, type: None, official_model_name: None]")
        resp = form.submit('Save RMA').maybe_follow()
        bs_doc = bs(resp.content)

        ul_list = bs_doc.findAll('ul')
        error_count = 0
        for u in ul_list:
            if u.has_attr('class'):
                if u['class'][0] == 'errorlist':
                    error_count += 1
        self.assertEqual(3, error_count)

        self.assertEqual('Please correct errors belowYOU MUST SELECT SOME ITEMS', bs_doc.p.get_text())

        # select a part with a quantity
        form = resp.forms["create-rma-with-an-existing-customer"]
        form['part_0'].select(text="[description: new part, model_number:None, type: None, official_model_name: None]")
        form['quantity_0'] = 5
        resp = form.submit('Save RMA').maybe_follow()
        bs_doc = bs(resp.content)

        ul_list = bs_doc.findAll('ul')
        error_count = 0
        for u in ul_list:
            if u.has_attr('class'):
                if u['class'][0] == 'errorlist':
                    error_count += 1

        # after selecting a site you get 4 messages
        # no case number
        # no reference number
        # no contact
        # * parts selected

        self.assertEqual(3, error_count)

        self.assertEqual('Please correct errors below', bs_doc.p.get_text())

        # add a date and get one fewer error
        form = resp.forms["create-rma-with-an-existing-customer"]
        form['date'] = '2014-11-30'
        resp = form.submit('Save RMA').maybe_follow()
        bs_doc = bs(resp.content)

        ul_list = bs_doc.findAll('ul')
        error_count = 0
        for u in ul_list:
            if u.has_attr('class'):
                if u['class'][0] == 'errorlist':
                    error_count += 1
        self.assertEqual(3, error_count)


        # after selecting a date and saleforce case number you get 2 messages
        # no case number
        # no reference number
        # no contact
        # * parts selected
        # add a case number and get one fewer error
        form = resp.forms["create-rma-with-an-existing-customer"]
        form['case_number'] = '1234'
        resp = form.submit('Save RMA').maybe_follow()
        bs_doc = bs(resp.content)

        ul_list = bs_doc.findAll('ul')
        error_count = 0
        for u in ul_list:
            if u.has_attr('class'):
                if u['class'][0] == 'errorlist':
                    error_count += 1
        self.assertEqual(2, error_count)

        # add a ref number for javascript and get one fewer error
        # no contact left
        form = resp.forms["create-rma-with-an-existing-customer"]
        form['reference_number'] = '1234'
        resp = form.submit('Save RMA').maybe_follow()
        bs_doc = bs(resp.content)

        ul_list = bs_doc.findAll('ul')
        error_count = 0
        for u in ul_list:
            if u.has_attr('class'):
                if u['class'][0] == 'errorlist':
                    error_count += 1
        self.assertEqual(1, error_count)

        # add a contact and get a successfully entered rma
        form = resp.forms["create-rma-with-an-existing-customer"]
        form['contact'] = 'bob'
        resp = form.submit('Save RMA').maybe_follow()
        bs_doc = bs(resp.content)

        div_list = bs_doc.findAll('div')
        # see if company was set right an saved
        company_count = 0
        for d in div_list:
            if d.has_attr('class'):
                if d['class'][0] == 'col-md-8' and d['class'][1] == 'data' and d.get_text() == 'new customer: new customer':
                    company_count += 1
        self.assertEqual(1, company_count)
        # see if contact was set to bob
        contact_count = 0
        for d in div_list:
            if d.has_attr('class'):
                if d['class'][0] == 'col-md-8' and d['class'][1] == 'data' and re.search('bob', d.get_text()) > 0:
                    contact_count += 1
        self.assertEqual(1, contact_count)
        # see if date was set to 2014-11-30
        date_count = 0
        for d in div_list:
            if d.has_attr('class'):
                if d['class'][0] == 'col-md-8' and d['class'][1] == 'data' and re.search('11/30/2014', d.get_text()) > 0:
                    date_count += 1
        self.assertEqual(1, date_count)
        # see if sales force number is 1234
        sf_num_count = 0
        for d in div_list:
            if d.has_attr('class'):
                if d['class'][0] == 'col-md-8' and d['class'][1] == 'data' and re.search('1234', d.get_text()) > 0:
                    sf_num_count += 1
        self.assertEqual(2, sf_num_count)  # it's in both the salesforce number and the reference number
