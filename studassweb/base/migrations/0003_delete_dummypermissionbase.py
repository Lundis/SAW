# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_dummypermissionbase'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DummyPermissionBase',
        ),
    ]
