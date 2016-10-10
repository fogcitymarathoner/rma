# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100)),
                ('note', models.TextField(max_length=300, null=True, blank=True)),
                ('model_number', models.CharField(max_length=90, null=True, blank=True)),
                ('type', models.CharField(max_length=90, null=True, blank=True)),
                ('last_modified_on', models.DateField(null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'Parts',
            },
            bases=(models.Model,),
        ),
    ]
