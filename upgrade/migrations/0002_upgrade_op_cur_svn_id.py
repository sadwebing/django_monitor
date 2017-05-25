# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upgrade_op',
            name='cur_svn_id',
            field=models.CharField(default=394, max_length=20),
            preserve_default=False,
        ),
    ]
