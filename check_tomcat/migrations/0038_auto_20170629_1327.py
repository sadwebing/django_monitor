# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0037_auto_20170628_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check_status',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
