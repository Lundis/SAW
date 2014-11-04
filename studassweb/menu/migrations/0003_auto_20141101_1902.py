# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20141101_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='template',
            field=models.ForeignKey(null=True, blank=True, to='menu.MenuTemplate'),
        ),
    ]
