# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0009_auto_20170701_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='op_history',
            name='info',
            field=models.TextField(max_length=51200, blank=True),
        ),
    ]
