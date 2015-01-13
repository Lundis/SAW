# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_userextension_can_apply_for_membership'),
        ('members', '0004_auto_20150111_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='user',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.AddField(
            model_name='member',
            name='user_ext',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, unique=True, to='users.UserExtension'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='payment',
            name='member',
            field=models.ForeignKey(default=1, to='members.Member'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='enrollment_year',
            field=models.IntegerField(default=2015),
            preserve_default=True,
        ),
    ]
