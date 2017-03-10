# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0008_auto_20170305_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='tomcat_url',
            name='status',
            field=models.CharField(default='active', max_length=20),
        ),
    ]
