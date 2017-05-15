# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0019_tomcat_url_server_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='tomcat_url',
            name='server_type',
            field=models.CharField(default='normal', max_length=10),
        ),
    ]
