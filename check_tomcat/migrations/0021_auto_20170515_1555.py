# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0020_tomcat_url_server_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tomcat_url',
            name='url',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='tomcat_url',
            unique_together=set([('project', 'server_ip')]),
        ),
    ]
