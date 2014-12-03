# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 3, 15, 59, 42, 320145)),
            preserve_default=True,
        ),
    ]
