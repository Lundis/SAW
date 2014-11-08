# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_delete_dummypermissionbase'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='association_founded',
            field=models.IntegerField(default=1900),
            preserve_default=True,
        ),
    ]
