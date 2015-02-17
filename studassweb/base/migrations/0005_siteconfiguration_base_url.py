# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20150207_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='base_url',
            field=models.CharField(max_length=150, default='http://localhost:8000'),
            preserve_default=True,
        ),
    ]
