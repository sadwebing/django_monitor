# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientservices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='malfunction',
            name='handle_user',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='malfunction',
            name='mal_status',
            field=models.CharField(default=b'\xe6\x9c\xaa\xe5\xa4\x84\xe7\x90\x86', max_length=128),
        ),
        migrations.AlterField(
            model_name='malfunction',
            name='record_user',
            field=models.CharField(max_length=128),
        ),
    ]
