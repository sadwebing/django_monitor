# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('clientservices', '0006_mal_history'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mal_history',
            old_name='op_info',
            new_name='op_after',
        ),
        migrations.AddField(
            model_name='mal_history',
            name='op_before',
            field=models.CharField(default=datetime.datetime(2017, 5, 7, 16, 33, 36, 401000), max_length=2048),
            preserve_default=False,
        ),
    ]
