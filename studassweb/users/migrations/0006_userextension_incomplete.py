# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150225_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextension',
            name='incomplete',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
