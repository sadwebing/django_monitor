# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0004_auto_20170524_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='svn_id',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_time', models.CharField(max_length=32)),
                ('svn_id', models.CharField(max_length=32)),
                ('tag', models.CharField(max_length=32, blank=True)),
                ('project', models.CharField(max_length=64)),
                ('cur_status', models.CharField(default=b'undone', max_length=16)),
                ('info', models.CharField(max_length=128, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='upgrade_op',
            name='id_time',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterUniqueTogether(
            name='svn_id',
            unique_together=set([('svn_id', 'project')]),
        ),
    ]
