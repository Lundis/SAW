# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_auto_20150221_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iteminevent',
            name='hide_in_print_view',
        ),
        migrations.RemoveField(
            model_name='iteminevent',
            name='public',
        ),
        migrations.AddField(
            model_name='eventitem',
            name='hide_in_print_view',
            field=models.BooleanField(default=False, verbose_name='Is this field hidden from the print view?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventitem',
            name='public',
            field=models.BooleanField(default=False, verbose_name='Is this field shown to everyone?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='permission',
            field=models.CharField(default='can_view_and_join_public_events', max_length=100, choices=[('can_view_and_join_public_events', 'Public event'), ('can_view_and_join_member_events', 'Members-only event'), ('can_view_and_join_board_member_events', 'Board members-only event')]),
            preserve_default=True,
        ),
    ]
