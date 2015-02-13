# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20150212_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventsignup',
            options={'ordering': ('created',)},
        ),
    ]
