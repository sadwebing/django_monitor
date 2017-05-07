# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientservices', '0005_auto_20170504_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='mal_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op_time', models.CharField(max_length=128)),
                ('op_user', models.CharField(max_length=128)),
                ('op_addr', models.CharField(max_length=32)),
                ('op_type', models.CharField(max_length=64)),
                ('op_info', models.CharField(max_length=2048)),
            ],
        ),
    ]
