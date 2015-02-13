# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_event_max_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='signup_start',
            field=models.DateTimeField(verbose_name='Signup starts', default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
