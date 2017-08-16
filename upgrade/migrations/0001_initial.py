# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='op_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('envir', models.CharField(max_length=10)),
                ('svn_id', models.CharField(max_length=20)),
                ('project', models.CharField(max_length=128)),
                ('ip_addr', models.GenericIPAddressField()),
                ('act', models.CharField(max_length=20)),
                ('op_time', models.CharField(max_length=64)),
                ('com_time', models.CharField(max_length=64)),
                ('op_user', models.CharField(max_length=64)),
                ('op_ip_addr', models.GenericIPAddressField()),
                ('op_status', models.IntegerField(default=0)),
                ('backup_file', models.CharField(max_length=128)),
                ('info', models.TextField(max_length=51200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='svn_id',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_time', models.CharField(max_length=32)),
                ('svn_id', models.CharField(max_length=32)),
                ('tag', models.CharField(max_length=32, blank=True)),
                ('project', models.CharField(max_length=64)),
                ('envir_uat', models.CharField(default=b'undone', max_length=16)),
                ('envir_online', models.CharField(default=b'undone', max_length=16)),
                ('deleted', models.IntegerField(default=0)),
                ('lock', models.IntegerField(default=0)),
                ('info', models.CharField(max_length=128, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='upgrade_cur_svn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.CharField(max_length=10)),
                ('project', models.CharField(unique=True, max_length=64)),
                ('cur_svn_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='upgrade_op',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('svn_id', models.CharField(max_length=20)),
                ('id_time', models.CharField(max_length=32)),
                ('project', models.CharField(max_length=64)),
                ('cur_status', models.CharField(max_length=16)),
                ('op_time', models.CharField(max_length=64)),
                ('handle_user', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='upgrade_cur_svn',
            unique_together=set([('product', 'project')]),
        ),
        migrations.AlterUniqueTogether(
            name='svn_id',
            unique_together=set([('svn_id', 'project')]),
        ),
    ]
