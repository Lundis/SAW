# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='user_ext',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, unique=True, to='users.UserExtension', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('first_name', 'last_name', 'email')]),
        ),
        migrations.AddField(
            model_name='customentry',
            name='field',
            field=models.ForeignKey(to='members.CustomField'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customentry',
            name='member',
            field=models.ForeignKey(to='members.Member'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='customentry',
            unique_together=set([('field', 'member')]),
        ),
    ]
