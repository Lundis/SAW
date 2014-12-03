# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20141130_2120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='type',
            new_name='created_by',
        ),
        migrations.AddField(
            model_name='menu',
            name='created_by',
            field=models.CharField(default='AP', choices=[('AP', 'Created by app'), ('US', 'Created by user')], max_length=2),
            preserve_default=True,
        ),
    ]
