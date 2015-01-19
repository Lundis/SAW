# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_auto_20141203_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='uploaded',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
