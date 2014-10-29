# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20141022_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disabledmodule',
            name='app_name',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
