# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20150220_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='permission',
            field=models.CharField(max_length=100, default='can_view_and_join_public_events', choices=[('can_view_and_join_public_events', 'Public event'), ('can_view_and_join_board_member_events', 'Members-only event'), ('can_view_and_join_board:member_events', 'Board members-only event')]),
            preserve_default=True,
        ),
    ]
