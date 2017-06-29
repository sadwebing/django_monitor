# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0031_check_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check_status',
            name='status',
            field=models.CharField(default='True', max_length=10),
        ),
    ]
