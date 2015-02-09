# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150204_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsignup',
            name='delete_confirmation_code',
            field=models.CharField(unique=True, max_length=32, default=''),
            preserve_default=False,
        ),
    ]
