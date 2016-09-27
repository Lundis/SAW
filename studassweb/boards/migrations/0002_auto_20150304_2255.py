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
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='members.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='boardmember',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='boards.Role'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='boardmember',
            unique_together={('board', 'role', 'member')},
        ),
        migrations.AddField(
            model_name='board',
            name='boardtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='boards.BoardType'),
            preserve_default=True,
        ),
    ]
