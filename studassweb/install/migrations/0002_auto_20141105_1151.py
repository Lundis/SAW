# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('install', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='installprogress',
            name='menu_ok',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='installprogress',
            name='modules_ok',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='installprogress',
            name='site_name_ok',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
