# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-14 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='search_text',
            field=models.TextField(blank=True, editable=False),
        ),
    ]
