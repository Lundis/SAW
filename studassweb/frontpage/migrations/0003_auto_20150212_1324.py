# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0002_auto_20150212_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontpageitem',
            name='ordering_index',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
    ]
