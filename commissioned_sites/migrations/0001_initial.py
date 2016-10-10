# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wireless_network_name', models.CharField(max_length=100, null=True, blank=True)),
                ('ssid', models.CharField(max_length=250, null=True, blank=True)),
                ('password', models.CharField(max_length=100, null=True, blank=True)),
                ('energy_manager_ip_address', models.CharField(max_length=100, null=True, blank=True)),
                ('energy_manager_username', models.CharField(max_length=100, null=True, blank=True)),
                ('energy_manager_password', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Wireless Networks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'From Salesforce', max_length=100)),
                ('address', models.TextField(max_length=700, null=True, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('contact', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_phone_number', models.CharField(max_length=100, null=True, blank=True)),
                ('cloud_ssh_tunnel_port', models.CharField(max_length=100, null=True, blank=True)),
                ('number_of_installed_energy_managers', models.IntegerField(default=0, null=True, blank=True)),
                ('number_of_installed_energy_managers_notes', models.CharField(max_length=100, null=True, blank=True)),
                ('number_of_installed_gateways', models.IntegerField(default=0, null=True, blank=True)),
                ('number_of_installed_sensor_units_and_control_units', models.IntegerField(default=0, null=True, blank=True)),
                ('number_of_installed_sensor_units_and_control_units_notes', models.CharField(max_length=100, null=True, blank=True)),
                ('number_of_installed_enlighted_room_controls', models.CharField(max_length=100, null=True, blank=True)),
                ('number_of_installed_enlighted_room_controls_notes', models.CharField(max_length=100, null=True, blank=True)),
                ('sensor_type', models.CharField(max_length=100, null=True, blank=True)),
                ('software_version_of_energy_manager', models.CharField(max_length=100, null=True, blank=True)),
                ('software_version_of_gateway', models.CharField(max_length=100, null=True, blank=True)),
                ('software_version_of_sensor_unit', models.CharField(max_length=100, null=True, blank=True)),
                ('profiles_file', models.FileField(help_text=b'Attach screenshot of all profiles used in a zipfile.', storage=django.core.files.storage.FileSystemStorage(location=b'/var/opt/rma/profiles/commissioned_sites/production'), upload_to=b'')),
                ('software_upgraded', models.PositiveSmallIntegerField(default=1, help_text=b'Includes EM, SU and Gateway', choices=[(2, b'Yes'), (1, b'No')])),
                ('sharepoint_origin', models.PositiveSmallIntegerField(default=0, help_text=b'From Sharepoint', choices=[(2, b'Yes'), (1, b'No')])),
                ('sharepoint_origin_url', models.CharField(max_length=200, null=True, blank=True)),
                ('last_modified_on', models.DateField(null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Commissioned Sites',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/var/opt/rma/attachments/commissioned_sites/production'), upload_to=b'')),
                ('site', models.ForeignKey(related_name='SiteAttachment.site', to='commissioned_sites.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='network',
            name='site',
            field=models.ForeignKey(to='commissioned_sites.Site'),
            preserve_default=True,
        ),
    ]
