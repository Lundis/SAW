# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_infocategory_menu_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infocategory',
            name='permission',
            field=models.CharField(max_length=15, default='VIEW_PUBLIC', choices=[('VIEW_PUBLIC', 'Can view public info pages'), ('VIEW_MEMBER', 'Can view member info pages'), ('VIEW_BOARD', 'Can view board member info pages')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='infopage',
            name='permission',
            field=models.CharField(max_length=100, default='VIEW_PUBLIC', choices=[('VIEW_PUBLIC', 'Can view public info pages'), ('VIEW_MEMBER', 'Can view member info pages'), ('VIEW_BOARD', 'Can view board member info pages')]),
            preserve_default=True,
        ),
    ]
