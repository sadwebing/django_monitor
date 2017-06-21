# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0028_tomcat_project_server_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tomcat_url',
            name='server_type',
        ),
    ]
