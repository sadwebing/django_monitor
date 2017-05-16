# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0021_auto_20170515_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tomcat_url',
            name='server_type',
            field=models.CharField(default='tomcat', max_length=10),
        ),
    ]
