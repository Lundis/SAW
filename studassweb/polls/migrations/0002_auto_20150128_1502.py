# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='permission',
            field=models.CharField(choices=[('CAN_VIEW_PUBLIC_POLLS', 'can_view_public_polls'), ('CAN_VIEW_MEMBER_POLLS', 'can_view_member_polls'), ('CAN_VIEW_BOARD_POLLS', 'can_view_board_polls'), ('CAN_VOTE_PUBLIC_POLLS', 'can_vote_public_polls'), ('CAN_VOTE_MEMBER_POLLS', 'can_vote_member_polls'), ('CAN_VOTE_BOARD_POLLS', 'can_vote_board_polls')], max_length=30, default='CAN_VIEW_PUBLIC_POLLS'),
            preserve_default=True,
        ),
    ]
