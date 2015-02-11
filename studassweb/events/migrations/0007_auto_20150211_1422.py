# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150211_0025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iteminevent',
            name='type',
        ),
        migrations.AddField(
            model_name='eventitem',
            name='required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventitem',
            name='type',
            field=models.CharField(choices=[('B', 'Boolean'), ('S', 'String'), ('T', 'Text'), ('I', 'Integer'), ('C', 'Choice')], max_length=1, default='I'),
            preserve_default=True,
        ),
    ]
