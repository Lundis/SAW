# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('menu', '0004_auto_20141101_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='view_permission',
            field=models.ForeignKey(to='auth.Permission', blank=True, null=True),
            preserve_default=True,
        ),
    ]
