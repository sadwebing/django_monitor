# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0025_auto_20170620_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tomcat_url',
            name='envir',
            field=models.CharField(default='ONLINE', max_length=10),
        ),
    ]
