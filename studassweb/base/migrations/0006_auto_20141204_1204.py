# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20141204_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfiguration',
            name='bootstrap_theme_mod_url',
            field=models.CharField(default='css/themes/bootstrap-theme.min.css', max_length=200, blank=True, null=True),
            preserve_default=True,
        ),
    ]
