# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import events.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150210_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='permission',
            field=models.CharField(max_length=100, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(unique=True, default='aaa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='iteminevent',
            name='type',
            field=models.CharField(max_length=1, default='I', choices=[('B', 'Boolean'), ('S', 'String'), ('I', 'Integer'), ('C', 'Choice')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='iteminsignup',
            name='value',
            field=events.models.MultiInputField(max_length=500, blank=True, null=True),
            preserve_default=True,
        ),
    ]
