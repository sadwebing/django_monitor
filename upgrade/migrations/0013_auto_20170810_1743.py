# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0012_auto_20170706_1740'),
    ]

    operations = [
        migrations.RenameField(
            model_name='svn_id',
            old_name='cur_status',
            new_name='envir_online',
        ),
        migrations.AddField(
            model_name='svn_id',
            name='envir_uat',
            field=models.CharField(default=b'undone', max_length=16),
        ),
    ]
