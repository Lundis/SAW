# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='infocategory',
            name='menu_item',
            field=models.ForeignKey(to='menu.MenuItem', null=True),
            preserve_default=True,
        ),
    ]
