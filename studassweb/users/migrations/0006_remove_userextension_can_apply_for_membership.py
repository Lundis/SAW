# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20141201_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userextension',
            name='can_apply_for_membership',
        ),
    ]
