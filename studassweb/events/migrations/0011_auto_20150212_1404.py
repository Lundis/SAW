# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20150211_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsignup',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
            preserve_default=True,
        ),
    ]
