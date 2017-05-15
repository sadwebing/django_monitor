# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0017_auto_20170513_0827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tomcat_url',
            name='server_ip',
        ),
    ]
