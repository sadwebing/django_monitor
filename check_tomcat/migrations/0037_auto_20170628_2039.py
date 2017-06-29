# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0036_auto_20170628_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='check_salt_minion',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mail',
            name='check_services',
            field=models.IntegerField(default=0),
        ),
    ]
