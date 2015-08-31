# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20150831_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSSMap',
            fields=[
                ('key', models.CharField(primary_key=True, max_length=50, unique=True, serialize=False)),
                ('value', models.CharField(max_length=250, default='')),
                ('default', models.CharField(max_length=250, default='')),
                ('default_has_changed', models.BooleanField(default=False)),
            ],
        ),
    ]
