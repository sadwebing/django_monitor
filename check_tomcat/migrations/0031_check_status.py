# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0030_tomcat_url_server_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='check_status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('program', models.CharField(max_length=16)),
                ('status', models.CharField(default=True, max_length=10)),
            ],
        ),
    ]
