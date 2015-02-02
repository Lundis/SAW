# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_infocategory_menu_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='infopage',
            name='for_frontpage',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
