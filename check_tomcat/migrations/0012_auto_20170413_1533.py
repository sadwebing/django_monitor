# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0011_tomcat_project_tomcat_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tomcat_project',
            name='tomcat_version',
            field=models.CharField(default='7', max_length=10, null=True),
        ),
    ]
