__author__ = 'marc'
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
import redis
import json

from django.conf import settings
from django.contrib.auth.models import Group

from return_merchandise_authorizations.models import Rma
from return_merchandise_authorizations.models import Item
from return_merchandise_authorizations.models import RmaAttachment
from parts.models import Part
from customers.models import Customer
from customers.models import CustomerCompany
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth.models import User
from returned_items.forms import get_part_choices

class SimpleTest(TestCase):

    def test_model(self):
        """
        Test the business rules of the returned_item model
        """
        new_part, created = Part.objects.get_or_create(description='new part')
        tst_user_username_good = 'tstuser_good'
        tst_user_pw_good = 'password_good'
        tst_user_email_good = 'email@email.com'

        user = User.objects.create_user(tst_user_username_good, tst_user_email_good, tst_user_pw_good)

        new_customer, created = CustomerCompany.objects.get_or_create(company_name='new customer')
        new_customer_site, created = Customer.objects.get_or_create(name='new customer', customer=new_customer)

        new_rma, created = Rma.objects.get_or_create(id=99999, last_modified_by=user, customer=new_customer_site, date= '2014-04-04', case_number='1234' ,reference_number='1234', contact='bob')
        new_item, created = Item.objects.get_or_create(part=new_part, quantity=2, rma=new_rma)
        attachment = RmaAttachment.objects.get_or_create(rma=new_rma, file=SimpleUploadedFile('best_file_eva.txt', 'these are the file contents!'))



        self.assertEqual('Return Merchanise Authorizations', new_rma._meta.verbose_name_plural)

        new_item = Item()
        new_attachment = RmaAttachment()

        choices = get_part_choices()
        self.assertEqual('1', choices[0][0])
        self.assertEqual('new part: None', choices[0][1])
