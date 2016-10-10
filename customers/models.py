from django.db import models
import redis
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from datetime import datetime as dt

from django.conf import settings
class CustomerCompany(models.Model):
    """
    The customer
    """
    company_name = models.CharField(max_length = 100, unique=True)

    last_modified_by = models.ForeignKey(User, null=True, blank=True)
    last_modified_on = models.DateField(null=True)

    def __unicode__(self):
        return '%s'%(
                    self.company_name
        )
    class Meta:
        verbose_name_plural = "Customers"

class Customer(models.Model):
    """
    The customer's site - It's mis-named unfortunately.
    """
    customer = models.ForeignKey(CustomerCompany, null=False)
    name = models.CharField(max_length = 100)

    last_modified_by = models.ForeignKey(User, null=True, blank=True)
    last_modified_on = models.DateField(null=True)
    def get_absolute_url(self):
        return reverse("view_customer", kwargs={"id": self.id})
    def __unicode__(self):
        return '%s: %s'%(
                    self.customer.company_name,
                    self.name
        )
    class Meta:
        verbose_name_plural = "Customer Sites"
        unique_together = ("customer", "name")

@receiver(pre_save, sender=Customer)
def customer_save_handler(sender, **kwargs):
    customer = kwargs['instance']
    customer.last_modified_on = dt.now()

@receiver(post_save, sender=Customer)
def customer_post_save_handler(sender, **kwargs):
    from xml_helpers.lib import load_customer_to_redis
    customer = kwargs['instance']

    r = redis.StrictRedis(host='localhost', port=6379, db=settings.REDIS_DB)
    load_customer_to_redis(customer, r)

@receiver(pre_delete, sender=CustomerCompany)
def customer_post_delete_handler(sender, **kwargs):
    customer = kwargs['instance']

    r = redis.StrictRedis(host='localhost', port=6379, db=settings.REDIS_DB)
    sites = Customer.objects.filter(customer=customer)
    for s in sites:
        r.delete(s.name)
@receiver(pre_delete, sender=Customer)
def customer_post_delete_handler(sender, **kwargs):
    customer = kwargs['instance']

    r = redis.StrictRedis(host='localhost', port=6379, db=settings.REDIS_DB)
    r.delete(customer.name)