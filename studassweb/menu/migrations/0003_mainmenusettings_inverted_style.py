# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20150128_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainmenusettings',
            name='inverted_style',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
