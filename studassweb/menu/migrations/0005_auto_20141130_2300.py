# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20141130_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='external_url',
            field=models.CharField(blank=True, max_length=200, null=True),
            preserve_default=True,
        ),
    ]
