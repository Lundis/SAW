# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20141022_1044'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='disabled_module',
            new_name='DisabledModule',
        ),
    ]
