# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20150222_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='permission',
        ),
        migrations.AddField(
            model_name='poll',
            name='permission_choice_view',
            field=models.CharField(max_length=100, verbose_name='Who can view this poll?', default='CAN_VIEW_PUBLIC_POLLS', choices=[('can_view_public_polls', 'Everyone'), ('can_view_member_polls', 'Members'), ('can_view_board_polls', 'The board')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='poll',
            name='permission_choice_vote',
            field=models.CharField(max_length=100, verbose_name='Who can vote on this poll?', default='CAN_VOTE_PUBLIC_POLLS', choices=[('can_vote_public_polls', 'Everyone'), ('can_vote_member_polls', 'Members'), ('can_vote_board_polls', 'The board')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='poll',
            name='publication',
            field=models.DateTimeField(verbose_name='Date published', auto_now_add=True),
            preserve_default=True,
        ),
    ]
