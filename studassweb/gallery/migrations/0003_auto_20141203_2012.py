# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20141203_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 3, 20, 12, 23, 959669)),
            preserve_default=True,
        ),
    ]
