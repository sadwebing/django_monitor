# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0008_op_history_op_ip_addr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='op_history',
            name='op_status',
            field=models.IntegerField(default=0),
        ),
    ]
