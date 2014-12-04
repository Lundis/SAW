# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20141203_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bootswatchtheme',
            name='name',
            field=models.CharField(unique=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bootswatchtheme',
            name='preview_image',
            field=models.ImageField(upload_to='base/bootswatch'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='bootstrap_theme_mod_url',
            field=models.CharField(null=True, default='css/themes/bootstrap-theme.min.css', max_length=200),
            preserve_default=True,
        ),
    ]
