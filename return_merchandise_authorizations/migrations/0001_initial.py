# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('parts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(max_length=300, null=True, blank=True)),
                ('quantity', models.IntegerField()),
                ('part', models.ForeignKey(to='parts.Part')),
            ],
            options={
                'verbose_name_plural': 'RMA Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('case_number', models.CharField(help_text=b'From Salesforce', unique=True, max_length=100)),
                ('reference_number', models.CharField(help_text=b'Date+SalesforceCaseNumber filled automatically', unique=True, max_length=100)),
                ('address', models.TextField(max_length=100, null=True, blank=True)),
                ('date', models.DateField(null=True)),
                ('contact', models.CharField(max_length=100, null=True)),
                ('contact_phone_number', models.CharField(max_length=100, null=True, blank=True)),
                ('issue', models.TextField(max_length=300, null=True, blank=True)),
                ('shipping', models.CharField(max_length=100, null=True)),
                ('outbound_tracking_number', models.CharField(max_length=100, null=True, blank=True)),
                ('return_tracking_number', models.CharField(max_length=100, null=True, blank=True)),
                ('root_cause_analysis', models.TextField(max_length=300, null=True, blank=True)),
                ('sharepoint_origin', models.PositiveSmallIntegerField(default=1, help_text=b'From Sharepoint', choices=[(2, b'Yes'), (1, b'No')])),
                ('sharepoint_origin_url', models.CharField(max_length=200, null=True, blank=True)),
                ('phase', models.PositiveSmallIntegerField(default=0, choices=[(1, b'Install'), (2, b'PostInstall')])),
                ('last_modified_on', models.DateField(null=True)),
                ('emailed', models.PositiveSmallIntegerField(default=1, choices=[(2, b'Yes'), (1, b'No')])),
                ('approved', models.PositiveSmallIntegerField(default=1, choices=[(2, b'Yes'), (1, b'No')])),
                ('approved_on', models.DateField(null=True)),
                ('approval_notes', models.TextField(max_length=500, null=True, blank=True)),
                ('approved_by', models.ForeignKey(related_name='rma.approver', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('customer', models.ForeignKey(to='customers.Customer')),
                ('last_modified_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Return Merchanise Authorizations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RmaAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/var/opt/rma/attachments/rma/production'), upload_to=b'')),
                ('rma', models.ForeignKey(to='return_merchandise_authorizations.Rma')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='item',
            name='rma',
            field=models.ForeignKey(to='return_merchandise_authorizations.Rma'),
            preserve_default=True,
        ),
    ]
