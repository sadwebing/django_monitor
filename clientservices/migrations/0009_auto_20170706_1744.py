# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientservices', '0008_auto_20170615_0744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mal_history',
            old_name='op_addr',
            new_name='op_ip_addr',
        ),
    ]
