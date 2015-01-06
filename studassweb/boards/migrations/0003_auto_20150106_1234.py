# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20141201_1402'),
        ('boards', '0002_auto_20141201_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='board',
            name='name',
        ),
        migrations.RemoveField(
            model_name='boardmember',
            name='user',
        ),
        migrations.RemoveField(
            model_name='role',
            name='board',
        ),
        migrations.AddField(
            model_name='board',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='boards.BoardType', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='boardmember',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='members.Member', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='boardmember',
            name='board',
            field=models.ForeignKey(to='boards.Board', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='boardmember',
            name='role',
            field=models.ForeignKey(to='boards.Role', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
    ]
