# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0006_tomcat_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tomcat_project',
            name='project',
            field=models.CharField(max_length=64),
        ),
    ]
