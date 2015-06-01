# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_auto_20150601_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='user_ext',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='users.UserExtension', null=True),
        ),
    ]
