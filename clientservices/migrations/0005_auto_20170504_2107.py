# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientservices', '0004_auto_20170504_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='malfunction',
            name='record_time',
            field=models.CharField(max_length=128),
        ),
    ]
