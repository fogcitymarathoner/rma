from django.db import models


from django.contrib.auth.models import User
from django.db import models

from django.core.urlresolvers import reverse

from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime as dt
from return_merchandise_authorizations.settings import YES_NO_CHOICES

class Part(models.Model):
    """
    Return Merchandise Authorization
    belongs to Customer
    """
    description = models.CharField(max_length = 100)
    note = models.TextField(max_length = 300, null=True, blank=True)
    model_number = models.CharField(max_length=90, blank=True, null=True)
    type = models.CharField(max_length=90, blank=True, null=True)
    official_model_name = models.CharField(max_length = 100, null=True, blank=True)
    part_number = models.CharField(max_length=90, blank=True, null=True)

    end_of_life = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES,  default=1) # no
    last_modified_by = models.ForeignKey(User, null=True, blank=True)
    last_modified_on = models.DateField(null=True)

    def get_absolute_url(self):
        return reverse("view_part", kwargs={"id": self.id})
    def __unicode__(self):
        return '[description: %s, model_number:%s, type: %s, official_model_name: %s]'%(
                    self.description, self.model_number, self.type, self.official_model_name,
        )
    class Meta:
        verbose_name_plural = "Parts"
        ordering = ["description", "model_number"]

@receiver(pre_save, sender=Part)
def part_save_handler(sender, **kwargs):
    part = kwargs['instance']
    part.last_modified_on = dt.now()