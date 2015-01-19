# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_auto_20150107_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infocategory',
            name='permission',
            field=models.CharField(default='VIEW_PUBLIC', max_length=15, choices=[('VIEW_PUBLIC', 'can_view_public_info_pages'), ('VIEW_MEMBER', 'can_view_member_info_pages'), ('VIEW_BOARD', 'can_view_board_member_info_pages')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='infopage',
            name='permission',
            field=models.CharField(default='VIEW_PUBLIC', max_length=100, choices=[('VIEW_PUBLIC', 'can_view_public_info_pages'), ('VIEW_MEMBER', 'can_view_member_info_pages'), ('VIEW_BOARD', 'can_view_board_member_info_pages')]),
            preserve_default=True,
        ),
    ]
