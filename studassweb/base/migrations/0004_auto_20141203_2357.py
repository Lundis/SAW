# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20141203_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bootswatchtheme',
            name='theme_path',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='bootstrap_theme_mod_url',
            field=models.CharField(max_length=200, default='css/themes/bootstrap-theme.min.css'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='bootstrap_theme_url',
            field=models.CharField(max_length=200, default='css/themes/bootstrap.min.css'),
            preserve_default=True,
        ),
    ]
