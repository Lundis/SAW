# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20150601_2002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='choice',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Option'),
        ),
    ]
