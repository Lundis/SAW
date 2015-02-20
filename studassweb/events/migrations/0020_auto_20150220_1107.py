# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_eventsignup_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='permission',
            field=models.CharField(default='PUBLIC', choices=[('PUBLIC', 'can_view_and_join_public_events'), ('MEMBER', 'can_view_and_join_board_member_events'), ('BOARD_MEMBER', 'can_view_and_join_board:member_events')], max_length=100),
            preserve_default=True,
        ),
    ]
