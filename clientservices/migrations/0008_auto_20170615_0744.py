# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientservices', '0007_auto_20170507_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mal_history',
            name='op_user',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='malfunction',
            name='record_user',
            field=models.CharField(max_length=20),
        ),
    ]
