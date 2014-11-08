# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_menuitem_view_permission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='view_permission',
            field=models.ForeignKey(to='users.SAWPermission', null=True, blank=True),
        ),
    ]
