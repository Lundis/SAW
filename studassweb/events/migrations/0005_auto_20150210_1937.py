# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_eventsignup_delete_confirmation_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventsignup',
            old_name='delete_confirmation_code',
            new_name='auth_code',
        ),
    ]
