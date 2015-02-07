# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20150128_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='can_vote_on_many',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
