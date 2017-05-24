# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='upgrade_op',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('svn_id', models.CharField(max_length=20)),
                ('id_time', models.CharField(max_length=64)),
                ('project', models.CharField(max_length=64)),
                ('cur_status', models.CharField(max_length=16)),
                ('op_time', models.CharField(max_length=64)),
                ('handle_user', models.CharField(max_length=64)),
            ],
        ),
    ]
