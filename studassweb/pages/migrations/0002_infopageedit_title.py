# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='infopageedit',
            name='title',
            field=models.CharField(max_length=50, default=''),
            preserve_default=False,
        ),
    ]
