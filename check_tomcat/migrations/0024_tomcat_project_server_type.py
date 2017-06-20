# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0023_tomcat_project_cur_svn_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tomcat_project',
            name='server_type',
            field=models.CharField(default='tomcat', max_length=10),
        ),
    ]
