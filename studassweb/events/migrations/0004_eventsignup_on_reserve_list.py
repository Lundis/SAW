# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-17 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20160417_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsignup',
            name='on_reserve_list',
            field=models.BooleanField(default=False),
        ),
    ]
