# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0005_auto_20170621_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='svn_id',
            name='delete',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='svn_id',
            name='lock',
            field=models.IntegerField(default=0),
        ),
    ]
