# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_squashed_0024_eventsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsignup',
            name='auth_code',
            field=models.CharField(unique=True, max_length=32),
            preserve_default=True,
        ),
    ]
