# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_auto_20150213_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsignup',
            name='order_id',
            field=models.IntegerField(validators=django.core.validators.MinValueValidator(1), default=1),
            preserve_default=True,
        ),
    ]
