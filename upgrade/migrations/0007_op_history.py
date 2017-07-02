# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0006_auto_20170629_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='op_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('svn_id', models.CharField(max_length=20)),
                ('project', models.CharField(max_length=128)),
                ('ip_addr', models.GenericIPAddressField()),
                ('act', models.CharField(max_length=20)),
                ('op_time', models.CharField(max_length=64)),
                ('op_name', models.CharField(max_length=64)),
                ('op_status', models.CharField(max_length=10)),
                ('envir', models.CharField(max_length=10)),
                ('info', models.CharField(max_length=51200, blank=True)),
            ],
        ),
    ]
