# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_menuitem_submenu'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='type',
            field=models.CharField(max_length=2, choices=[('AP', 'Created by app'), ('US', 'Created by user')], default='AP'),
            preserve_default=True,
        ),
    ]
