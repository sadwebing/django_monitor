# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0026_auto_20170620_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tomcat_project',
            name='server_type',
        ),
    ]
