from django.db import models
from customers.models import Customer
from parts.models import Part
from return_merchandise_authorizations.settings import PHASE_CHOICES

from return_merchandise_authorizations.settings import YES_NO_CHOICES
from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings


from django.db.models.signals import post_save
from django.dispatch import receiver
from xml_helpers.lib import load_customer_to_redis
from django.conf import settings
import redis
from garage.logger import logger
class Rma(models.Model):
    """
    Return Merchandise Authorization
    belongs to CustomerSite
    """

    customer = models.ForeignKey(Customer) # actually a customer-SITE
    case_number = models.CharField(max_length = 100, help_text='From Salesforce')
    reference_number = models.CharField(max_length = 100, unique=True, help_text='Date+SalesforceCaseNumber filled automatically')
    address = models.TextField(max_length = 100, null=True, blank=True)
    date = models.DateField(null=True)
    contact = models.CharField(max_length = 100, null=True)
    contact_phone_number = models.CharField(max_length = 100, null=True, blank=True)
    issue = models.TextField(max_length = 300, null=True, blank=True)
    shipping = models.CharField(max_length = 100, null=True)
    outbound_tracking_number = models.CharField(max_length = 100, null=True, blank=True)
    return_tracking_number = models.CharField(max_length = 100, null=True, blank=True)

    root_cause_analysis = models.TextField(max_length = 300, null=True, blank=True)

    sharepoint_origin = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES, help_text='From Sharepoint', default=1)
    sharepoint_origin_url = models.CharField(max_length = 200, blank=True, null=True)

    phase = models.PositiveSmallIntegerField(choices=PHASE_CHOICES, default=0)

    last_modified_by = models.ForeignKey(User, null=True, blank=True)
    last_modified_on = models.DateField(null=True)


    emailed = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES,  default=1) # no

    approved = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES,  default=1) # no
    approved_by = models.ForeignKey(User, null=True, blank=True, related_name='rma.approver')
    approved_on = models.DateField(null=True)
    approval_notes = models.TextField(max_length = 500, null=True, blank=True)
    repair_costs = models.FloatField(null=True, blank=True, default=0.0)

    def __unicode__(self):
        return '[date: %s;number: %s; customer: %s]'%(
                    self.date,
                    self.case_number,
                    self.customer.name,
        )
    class Meta:
        verbose_name_plural = "Return Merchanise Authorizations"

@receiver(post_save, sender=Rma)
def rebuild_rma_cache_handler(sender, **kwargs):
    r = redis.StrictRedis(host='localhost', port=6379, db=settings.REDIS_DB)
    rma = kwargs['instance']
    # rebuild the ajax cache
    load_customer_to_redis(rma.customer, r)

my_store = FileSystemStorage(location=settings.RMA_ATTACHMENTS_DIR)
class RmaAttachment(models.Model):

    rma = models.ForeignKey(Rma)
    file = models.FileField(storage=my_store)


class Item(models.Model):
    """
    Items
    belongs to Return Merchanise Authorization
    """
    note = models.TextField(max_length = 300, null=True, blank=True)
    quantity = models.IntegerField()
    rma = models.ForeignKey(Rma)
    part = models.ForeignKey(Part)

    def __unicode__(self):
        return '%s | %s | %s | %s'%(
                    self.part.id,self.part.description, str(self.quantity), self.part.model_number
        )
    class Meta:
        verbose_name_plural = "RMA Items"
        ordering = ["-rma__date", "rma__customer__name"]

@receiver(post_save, sender=Rma)
def rma_post_save_handler(sender, **kwargs):
    """
    update ALL customers in redis database upon save.
    cannot just update single customer because old customer moved from will not update.
    can surgically update 2 customers (source and dest) but source is lost.
    :param sender:
    :param kwargs:
    :return:
    """
    from xml_helpers.lib import load_customer_to_redis
    r = redis.StrictRedis(host='localhost', port=6379, db=settings.REDIS_DB)
    customers = Customer.objects.all()

    for c in customers:
        load_customer_to_redis(c, r)