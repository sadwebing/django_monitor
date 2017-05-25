# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0002_upgrade_op_cur_svn_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='upgrade_cur_svn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.CharField(max_length=64)),
                ('cur_svn_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='upgrade_op',
            name='cur_svn_id',
        ),
    ]
