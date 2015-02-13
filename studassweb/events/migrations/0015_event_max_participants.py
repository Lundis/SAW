# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20150212_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='max_participants',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=50),
            preserve_default=True,
        ),
    ]
