# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0034_auto_20170628_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='check_salt_minion',
            field=models.CharField(default='false', max_length=5),
        ),
        migrations.AddField(
            model_name='mail',
            name='check_services',
            field=models.CharField(default='false', max_length=5),
        ),
        migrations.AlterField(
            model_name='check_status',
            name='status',
            field=models.CharField(default='true', max_length=5),
        ),
    ]
