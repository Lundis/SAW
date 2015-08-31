# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_cssmap'),
    ]

    operations = [
        migrations.AddField(
            model_name='cssmap',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
