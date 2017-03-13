# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0009_tomcat_url_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tomcat_project',
            name='project',
            field=models.CharField(unique=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='tomcat_project',
            name='status',
            field=models.CharField(default='active', max_length=10, null=True),
        ),
    ]
