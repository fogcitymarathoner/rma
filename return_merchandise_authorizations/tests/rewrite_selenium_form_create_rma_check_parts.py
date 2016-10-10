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

from customers.models import CustomerCompany
class WebTest(WebTest):
    """
    There no rythm or reason to how the parts from an RMA form are reassembled.
    id_part_name_3 could be before id_part_name1 in the request['POST'] dictionary
    """
    def test_rma_email_sent(self):
        """
        Test RMA Create form make sure parts-parts assemble right
        """

        g = Group(name='admin')
        g.save()
        g = Group(name='approver')
        g.save()
        g = Group(name='poweruser')
        g.save()
        g = Group(name='user')
        g.save()

        new_customer, created = CustomerCompany.objects.get_or_create(company_name='new customer')
        new_customer_site, created = Customer.objects.get_or_create(name='new customer', customer=new_customer)

        new_part, created = Part.objects.get_or_create(description='new part1')
        new_part, created = Part.objects.get_or_create(description='new part2')
        new_part, created = Part.objects.get_or_create(description='new part3')
        tst_user_username_good = 'tstuser_good'
        tst_user_pw_good = 'password_good'
        tst_user_email_good = 'email@email.com'

        user = User.objects.create_user(tst_user_username_good, tst_user_email_good, tst_user_pw_good)

        g = Group.objects.get(name='user')
        g.user_set.add(user)
        c0_url = reverse('home_page')

        resp = self.app.get(c0_url).maybe_follow()
        form = resp.forms['login-form']
        form['username'] = tst_user_username_good
        form['password'] = tst_user_pw_good

        form.submit('submit').follow()

        url = reverse('create_rma')

        resp = self.app.get(url).maybe_follow()


        form = resp.forms["create-rma-with-an-existing-customer"]
        form['name'] = new_customer_site.id
        #print form
        #quit()

        form['part_0'].select(text="[description: new part2, model_number:None, type: None, official_model_name: None]")
        form['quantity_0'] = 1
        form['note_0'] = "notes 1"

        form['part_1'].select(text="[description: new part2, model_number:None, type: None, official_model_name: None]")
        form['quantity_1'] = 2
        form['note_1'] = "notes 2"

        form['part_2'].select(text="[description: new part3, model_number:None, type: None, official_model_name: None]")
        form['quantity_2'] = 3
        form['note_2'] = "notes 3"
        form['date'] = '2014-11-30'
        form['case_number'] = '1234'
        form['reference_number'] = '1234'
        form['contact'] = 'bob'

        resp = form.submit('Save RMA').maybe_follow()

        # fix me this works with an actual browser, but not here