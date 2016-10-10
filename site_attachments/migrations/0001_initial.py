# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('commissioned_sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/var/opt/rma/attachments/commissioned_sites/production'), upload_to=b'')),
                ('site', models.ForeignKey(to='commissioned_sites.Site')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
