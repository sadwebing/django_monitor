# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0024_tomcat_project_server_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tomcat_url',
            old_name='server_ip',
            new_name='minion_id',
        ),
        migrations.AddField(
            model_name='tomcat_url',
            name='envir',
            field=models.CharField(default='UAT', max_length=10),
        ),
        migrations.AddField(
            model_name='tomcat_url',
            name='ip_addr',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tomcat_url',
            unique_together=set([('project', 'minion_id')]),
        ),
    ]
