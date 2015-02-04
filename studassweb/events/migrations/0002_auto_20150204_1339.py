# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsignup',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventsignup',
            name='diet',
            field=models.CharField(blank=True, max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventsignup',
            name='other',
            field=models.CharField(blank=True, max_length=200, null=True),
            preserve_default=True,
        ),
    ]
