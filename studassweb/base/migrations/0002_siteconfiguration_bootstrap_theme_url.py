# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='bootstrap_theme_url',
            field=models.CharField(max_length=200, default='css/bootstrap.min.css'),
            preserve_default=True,
        ),
    ]
