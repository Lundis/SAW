# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20150128_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='user_ext',
            field=models.ForeignKey(to='users.UserExtension', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, unique=True),
            preserve_default=True,
        ),
    ]
