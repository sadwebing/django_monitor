# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0015_project_servers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project_servers',
            old_name='script',
            new_name='info',
        ),
        migrations.AddField(
            model_name='project_servers',
            name='status',
            field=models.CharField(default='active', max_length=20),
        ),
    ]
