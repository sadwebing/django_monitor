# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 06:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0007_auto_20170305_1421'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tomcat_project',
            unique_together=set([('product', 'project')]),
        ),
    ]
