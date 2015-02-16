# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20150211_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infocategory',
            name='menu_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='menu.MenuItem', null=True),
            preserve_default=True,
        ),
    ]
