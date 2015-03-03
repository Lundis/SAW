# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20150215_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='identifier',
            field=models.CharField(unique=True, help_text='A unique identifier that is used to distinguish this item', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='submenu',
            field=models.ForeignKey(null=True, to='menu.Menu', blank=True),
            preserve_default=True,
        ),
    ]
