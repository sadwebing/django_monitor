# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0010_auto_20170702_1239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='svn_id',
            old_name='delete',
            new_name='deleted',
        ),
    ]
