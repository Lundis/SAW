# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardmember',
            name='member',
            field=models.ForeignKey(to='members.Member', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='boardmember',
            name='role',
            field=models.ForeignKey(to='boards.Role', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='boardmember',
            unique_together=set([('board', 'role', 'member')]),
        ),
        migrations.AddField(
            model_name='board',
            name='boardtype',
            field=models.ForeignKey(to='boards.BoardType', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
    ]
