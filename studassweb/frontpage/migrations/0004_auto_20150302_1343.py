# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0003_auto_20150212_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontpageitem',
            name='module',
            field=models.CharField(max_length=50, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='frontpageitem',
            name='render_function',
            field=models.CharField(max_length=50, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='frontpageitem',
            name='template',
            field=models.CharField(max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='frontpageitem',
            name='content',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
