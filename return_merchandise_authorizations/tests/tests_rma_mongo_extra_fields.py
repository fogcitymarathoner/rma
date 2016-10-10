__author__ = 'marc'
"""
It's not possible for the mongo test database to not  be influenced by these tests
"""
from django.test import TestCase
import redis
import json

from django.conf import settings
from django.contrib.auth.models import Group

from return_merchandise_authorizations.models import Rma
from return_merchandise_authorizations.models import Item
from return_merchandise_authorizations.models import RmaAttachment
from return_merchandise_authorizations.views import _sync_mongo_keys
from parts.models import Part
from customers.models import Customer
from customers.models import CustomerCompany
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth.models import User
from pymongo import MongoClient
class SimpleTest(TestCase):

    def setUp(self):
        g = Group(name='admin')
        g.save()
        g = Group(name='approver')
        g.save()
        g = Group(name='poweruser')
        g.save()
        g = Group(name='user')
        g.save()

        rfields = [{
                        'value': 'a'
                    }]
        r = redis.StrictRedis(host='localhost', port=6379, db=settings.SESSION_REDIS_DB)
        r.set(settings.SUB_URL.replace('/','')+':rma_extra_data', json.dumps(rfields))
    def tearDown(self):
        pass

    def test_mongo_fields(self):
        """
        Return Merchandise Authorizations - Test that the field names can be pulled from redis
        creating new rma should result in an empty 'a' field
        """


        r = redis.StrictRedis(host='localhost', port=6379, db=settings.SESSION_REDIS_DB)
        rfields = json.loads(r.get(settings.SUB_URL.replace('/','')+':rma_extra_data'))
        print rfields
        self.assertEqual('a', rfields[0]['value'])


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



        client = MongoClient()
        db = client[settings.MONGO_DB]
        extra_data = db.extra_data

        rma_extra_data = extra_data.find_one({"rma_id": new_rma.id})
        if rma_extra_data != None:
            extra_data.remove(rma_extra_data)
        rma_extra_data = extra_data.find_one({"rma_id": new_rma.id})
        self.assertEqual(None, rma_extra_data)
        # the accessor in view
        view_rma_extra_data = _sync_mongo_keys(new_rma.id)

        rma_extra_data = extra_data.find_one({"rma_id": new_rma.id})
        print rma_extra_data

        self.assertEqual('', rma_extra_data['a'])
        # the test database will have a rma with id of 1, so we will have to pick an out of range id like 99999