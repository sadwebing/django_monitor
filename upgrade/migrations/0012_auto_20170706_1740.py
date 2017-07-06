# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upgrade', '0011_auto_20170702_1736'),
    ]

    operations = [
        migrations.RenameField(
            model_name='op_history',
            old_name='op_name',
            new_name='op_user',
        ),
    ]
