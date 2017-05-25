# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0022_auto_20170516_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='tomcat_project',
            name='cur_svn_id',
            field=models.CharField(default='null', max_length=20),
            preserve_default=False,
        ),
    ]
