# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20150111_1707'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customfield',
            options={'ordering': ('name',)},
        ),
    ]
