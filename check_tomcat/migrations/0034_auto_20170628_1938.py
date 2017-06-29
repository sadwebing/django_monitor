# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0033_auto_20170628_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check_status',
            name='program',
            field=models.CharField(max_length=32),
        ),
    ]
