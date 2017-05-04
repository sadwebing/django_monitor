# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='malfunction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record_time', models.CharField(max_length=128)),
                ('mal_details', models.CharField(max_length=2048)),
                ('record_user', models.CharField(unique=True, max_length=128)),
                ('mal_reasons', models.CharField(max_length=2048)),
                ('mal_status', models.CharField(max_length=128)),
                ('recovery_time', models.CharField(max_length=128)),
                ('time_all', models.CharField(max_length=128)),
                ('handle_user', models.CharField(unique=True, max_length=128)),
            ],
        ),
    ]
