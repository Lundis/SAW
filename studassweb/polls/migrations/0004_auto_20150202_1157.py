# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_poll_can_vote_on_many'),
    ]

    operations = [
        migrations.RenameField(
            model_name='votes',
            old_name='members_choice',
            new_name='user',
        ),
    ]
