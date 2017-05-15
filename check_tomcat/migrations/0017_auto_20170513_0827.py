# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0016_auto_20170512_2109'),
    ]

    operations = [
        migrations.DeleteModel(
            name='project_servers',
        ),
        migrations.AddField(
            model_name='tomcat_url',
            name='info',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='tomcat_url',
            name='role',
            field=models.CharField(default='backup', max_length=16),
        ),
        migrations.AddField(
            model_name='tomcat_url',
            name='server_ip',
            field=models.CharField(default=datetime.datetime(2017, 5, 13, 8, 27, 30, 978000), max_length=32),
            preserve_default=False,
        ),
    ]
