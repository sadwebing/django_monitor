# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientservices', '0003_auto_20170504_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='malfunction',
            name='record_time',
            field=models.DateField(),
        ),
    ]
