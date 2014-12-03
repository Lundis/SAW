# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_siteconfiguration_bootstrap_theme_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='BootswatchTheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('theme_path', models.CharField(default='css/bootstrap.min.css', max_length=200)),
                ('preview_image', models.ImageField(upload_to='base/theme_previews')),
                ('preview_url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='bootstrap_theme_mod_url',
            field=models.CharField(default='css/bootstrap-theme.min.css', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='bootswatch_last_checked',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='bootswatch_version',
            field=models.CharField(default=None, null=True, max_length=50),
            preserve_default=True,
        ),
    ]
