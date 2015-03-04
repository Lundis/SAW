# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.fields
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('polls', '0001_initial'), ('polls', '0002_auto_20150128_1502'), ('polls', '0003_poll_can_vote_on_many'), ('polls', '0004_auto_20150202_1157'), ('polls', '0005_votes_ip_address'), ('polls', '0006_auto_20150222_1631'), ('polls', '0007_auto_20150302_1343')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', base.fields.ValidatedRichTextField(max_length=300)),
                ('publication', models.DateTimeField(auto_now_add=True, verbose_name='Date published')),
                ('expiration', models.DateTimeField(verbose_name='Poll closes')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('can_vote_on_many', models.BooleanField(default=False)),
                ('permission_choice_view', models.CharField(verbose_name='Who can view this poll?', max_length=100, default='CAN_VIEW_PUBLIC_POLLS', choices=[('can_view_public_polls', 'Everyone'), ('can_view_member_polls', 'Members'), ('can_view_board_polls', 'The board')])),
                ('permission_choice_vote', models.CharField(verbose_name='Who can vote on this poll?', max_length=100, default='CAN_VOTE_PUBLIC_POLLS', choices=[('can_vote_public_polls', 'Everyone'), ('can_vote_member_polls', 'Members'), ('can_vote_board_polls', 'The board')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('choice_id', models.ForeignKey(to='polls.Choice')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('ip_address', models.IPAddressField(default=None)),
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
