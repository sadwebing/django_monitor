# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0003_auto_20170524_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='upgrade_cur_svn',
            name='product',
            field=models.CharField(default='B79', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='upgrade_cur_svn',
            name='project',
            field=models.CharField(unique=True, max_length=64),
        ),
        migrations.AlterUniqueTogether(
            name='upgrade_cur_svn',
            unique_together=set([('product', 'project')]),
        ),
    ]
