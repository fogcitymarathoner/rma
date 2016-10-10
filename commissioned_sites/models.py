from django.db import models
from return_merchandise_authorizations.settings import YES_NO_CHOICES

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver

from garage.logger import logger
profile_store = FileSystemStorage(location=settings.COMMISSIONED_SITES_PROFILES_DIR)
class CommissionedSite(models.Model):
    """
    Commissioned Site
    """

    name = models.CharField(max_length = 100)
    address = models.TextField(max_length = 700, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length = 100, null=True, blank=True)
    contact_phone_number = models.CharField(max_length = 100, null=True, blank=True)
    cloud_ssh_tunnel_port = models.CharField(max_length = 100, null=True, blank=True)

    #
    number_of_installed_energy_managers = models.IntegerField(blank=True, null=True, default=0)
    number_of_installed_energy_managers_notes = models.CharField(max_length = 100, blank=True, null=True)

    number_of_installed_gateways = models.IntegerField(blank=True, null=True, default=0)
    #
    number_of_installed_sensor_units_and_control_units = models.IntegerField(blank=True, null=True, default=0)
    number_of_installed_sensor_units_and_control_units_notes = models.CharField(max_length = 100, blank=True, null=True)
    #
    number_of_installed_enlighted_room_controls = models.CharField(max_length = 100, blank=True, null=True)
    number_of_installed_enlighted_room_controls_notes = models.CharField(max_length = 100, blank=True, null=True)

    sensor_type = models.CharField(max_length = 100, null=True, blank=True)

    software_version_of_energy_manager = models.CharField(max_length = 100, null=True, blank=True)
    software_version_of_gateway = models.CharField(max_length = 100, null=True, blank=True)
    software_version_of_sensor_unit = models.CharField(max_length = 100, null=True, blank=True)

    profiles_file = models.FileField(storage=profile_store, help_text='Attach screenshot of all profiles used in a zipfile.', null=True, blank=True)
    software_upgraded = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES, help_text='Includes EM, SU and Gateway', default=1)

    sharepoint_origin = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES, help_text='From Sharepoint', default=0)
    sharepoint_origin_url = models.CharField(max_length = 200, blank=True, null=True)

    notes = models.TextField(max_length = 300, null=True, blank=True)
    last_modified_by = models.ForeignKey(User, null=True, blank=True)
    last_modified_on = models.DateField(null=True)

    def __unicode__(self):
        return '[name: %s]'%(
                    self.name,
        )
    class Meta:
        verbose_name_plural = "Commissioned Sites"
        ordering = ["-date"]

class Network(models.Model):
    """
    Network
    belongs to Commissioned Site (Site)
    """
    wireless_network_name = models.CharField(max_length = 100,blank=True, null=True)
    ssid = models.CharField(max_length = 250, blank=True, null=True)
    password = models.CharField(max_length = 100, null=True, blank=True)
    energy_manager_ip_address = models.CharField(max_length = 100, null=True, blank=True)
    energy_manager_username = models.CharField(max_length = 100, null=True, blank=True)
    energy_manager_password = models.CharField(max_length = 100, null=True, blank=True)

    site = models.ForeignKey(CommissionedSite)

    def __unicode__(self):
        return '[wireless_network_name: %s]'%(
                    self.wireless_network_name,
        )
    class Meta:
        verbose_name_plural = "Wireless Networks"
        ordering = ["wireless_network_name"]

my_store = FileSystemStorage(location=settings.COMMISSIONED_SITES_ATTACHMENTS_DIR)

class SiteAttachment(models.Model):

    site = models.ForeignKey(CommissionedSite, related_name='SiteAttachment.site')
    file = models.FileField(storage=my_store)


@receiver(post_save, sender=CommissionedSite)
def handle_new_job(sender, **kwargs):
    site = kwargs.get('instance')
    logger().debug("POST_SAVE : site : %s" % site)
    # find people to email based on `job` instance