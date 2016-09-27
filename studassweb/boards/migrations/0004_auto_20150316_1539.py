# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20150311_1258'),
        ('boards', '0003_auto_20150304_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberInBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('photo', models.ImageField(blank=True, upload_to='boards/photos', null=True)),
                ('board', models.ForeignKey(to='boards.Board', on_delete=django.db.models.deletion.PROTECT)),
                ('member', models.ForeignKey(to='members.Member', on_delete=django.db.models.deletion.PROTECT)),
                ('role', models.ForeignKey(to='boards.Role', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='boardmember',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='boardmember',
            name='board',
        ),
        migrations.RemoveField(
            model_name='boardmember',
            name='member',
        ),
        migrations.RemoveField(
            model_name='boardmember',
            name='role',
        ),
        migrations.DeleteModel(
            name='BoardMember',
        ),
        migrations.AlterUniqueTogether(
            name='memberinboard',
            unique_together={('board', 'role', 'member')},
        ),
        migrations.AddField(
            model_name='boardtype',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='role',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
    ]
