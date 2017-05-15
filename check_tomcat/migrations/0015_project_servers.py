# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('check_tomcat', '0014_auto_20170512_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='project_servers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.CharField(max_length=64)),
                ('role', models.CharField(default='backup', max_length=16)),
                ('server_ip', models.IPAddressField()),
                ('script', models.CharField(max_length=128, null=True)),
            ],
        ),
    ]
