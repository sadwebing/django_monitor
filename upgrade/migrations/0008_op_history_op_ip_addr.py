# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0007_op_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='op_history',
            name='op_ip_addr',
            field=models.GenericIPAddressField(default='127.0.0.1'),
            preserve_default=False,
        ),
    ]
