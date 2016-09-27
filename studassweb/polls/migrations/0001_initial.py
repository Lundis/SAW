# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', base.fields.ValidatedRichTextField(max_length=300)),
                ('publication', models.DateTimeField(verbose_name='Date published', auto_now_add=True)),
                ('expiration', models.DateTimeField(verbose_name='Poll closes')),
                ('can_vote_on_many', models.BooleanField(default=False)),
                ('permission_choice_view', models.CharField(
                    choices=[('can_view_public_polls', 'Everyone'),
                             ('can_view_member_polls', 'Members'),
                             ('can_view_board_polls', 'The board')],
                    verbose_name='Who can view this poll?', default='CAN_VIEW_PUBLIC_POLLS', max_length=100)),
                ('permission_choice_vote', models.CharField(
                    choices=[('can_vote_public_polls', 'Everyone'),
                             ('can_vote_member_polls', 'Members'),
                             ('can_vote_board_polls', 'The board')],
                    verbose_name='Who can vote on this poll?', default='CAN_VOTE_PUBLIC_POLLS', max_length=100)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('ip_address', models.IPAddressField(default=None)),
                ('choice_id', models.ForeignKey(to='polls.Choice')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
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
