# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_sawpermission_default_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='sawpermission',
            name='module',
            field=models.CharField(max_length=100, default='unset (run install!!)'),
            preserve_default=False,
        ),
    ]
