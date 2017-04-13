# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0010_auto_20170313_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='tomcat_project',
            name='tomcat_version',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
