# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_auto_20141202_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menutemplate',
            name='path',
            field=models.CharField(max_length=10, unique=True, choices=[('simple', 'menu/menus/simple.html'), ('standard', 'menu/menus/simple.html')], default='standard'),
            preserve_default=True,
        ),
    ]
