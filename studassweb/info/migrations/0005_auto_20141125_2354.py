# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_auto_20141124_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='infocategory',
            name='permission',
            field=models.CharField(choices=[('Guest', 'can_view_public_info_pages'), ('Member', 'can_view_member_info_pages'), ('Board Member', 'can_view_board_member_info_pages')], default='Guest', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='infopage',
            name='permission',
            field=models.CharField(choices=[('Guest', 'can_view_public_info_pages'), ('Member', 'can_view_member_info_pages'), ('Board Member', 'can_view_board_member_info_pages')], default='Guest', max_length=100),
            preserve_default=True,
        ),
    ]
