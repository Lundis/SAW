# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20141110_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='submenu',
            field=models.ForeignKey(null=True, to='menu.Menu'),
            preserve_default=True,
        ),
    ]
