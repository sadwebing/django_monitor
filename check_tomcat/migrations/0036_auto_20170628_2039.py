# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0035_auto_20170628_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='check_salt_minion',
        ),
        migrations.RemoveField(
            model_name='mail',
            name='check_services',
        ),
    ]
