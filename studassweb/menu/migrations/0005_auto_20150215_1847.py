# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_menu_item_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='identifier',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
