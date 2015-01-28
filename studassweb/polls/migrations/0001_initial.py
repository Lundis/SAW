# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300)),
                ('publication', models.DateTimeField(verbose_name='Date published')),
                ('expiration', models.DateTimeField(verbose_name='Poll closes')),
                ('permission', models.CharField(default='VIEW_PUBLIC', choices=[('CAN_VIEW_PUBLIC_POLLS', 'can_view_public_polls'), ('CAN_VIEW_MEMBER_POLLS', 'can_view_member_polls'), ('CAN_VIEW_BOARD_POLLS', 'can_view_board_polls'), ('CAN_VOTE_PUBLIC_POLLS', 'can_vote_public_polls'), ('CAN_VOTE_MEMBER_POLLS', 'can_vote_member_polls'), ('CAN_VOTE_BOARD_POLLS', 'can_vote_board_polls')], max_length=15)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('choice_id', models.ForeignKey(to='polls.Choice')),
                ('members_choice', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='choice',
            name='id_to_poll',
            field=models.ForeignKey(to='polls.Poll'),
            preserve_default=True,
        ),
    ]
