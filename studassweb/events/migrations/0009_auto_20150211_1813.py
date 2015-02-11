# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_remove_iteminsignup_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventsignup',
            name='association',
        ),
        migrations.RemoveField(
            model_name='eventsignup',
            name='diet',
        ),
        migrations.RemoveField(
            model_name='eventsignup',
            name='matricle',
        ),
        migrations.RemoveField(
            model_name='eventsignup',
            name='other',
        ),
    ]
