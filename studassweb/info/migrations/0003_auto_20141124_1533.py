# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_menuitem_type'),
        ('info', '0002_auto_20141120_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infocategory',
            name='submenu',
        ),
        migrations.AddField(
            model_name='infocategory',
            name='menu_item',
            field=models.ForeignKey(null=True, to='menu.MenuItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infopage',
            name='category',
            field=models.ForeignKey(null=True, to='info.InfoCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='infocategory',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
