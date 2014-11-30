# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextension',
            name='avatar',
            field=models.ImageField(default='users/avatars/default_avatar.png', upload_to='users/avatars'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userextension',
            name='member',
            field=models.ForeignKey(unique=True, to='members.Member', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
    ]
