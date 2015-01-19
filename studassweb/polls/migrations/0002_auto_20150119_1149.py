# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='created_by',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poll',
            name='permission',
            field=models.CharField(choices=[('CAN_VIEW_PUBLIC_POLLS', 'can_view_public_polls'), ('CAN_VIEW_MEMBER_POLLS', 'can_view_member_polls'), ('CAN_VIEW_BOARD_POLLS', 'can_view_board_polls'), ('CAN_VOTE_PUBLIC_POLLS', 'can_vote_public_polls'), ('CAN_VOTE_MEMBER_POLLS', 'can_vote_member_polls'), ('CAN_VOTE_BOARD_POLLS', 'can_vote_board_polls')], default='VIEW_PUBLIC', max_length=15),
            preserve_default=True,
        ),
    ]
