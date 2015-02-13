# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_event_signup_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='iteminevent',
            name='hide_in_print_view',
            field=models.BooleanField(verbose_name='Is this field hidden from the print view?', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='iteminevent',
            name='public',
            field=models.BooleanField(verbose_name='Is this field shown to everyone?', default=False),
            preserve_default=True,
        ),
    ]
