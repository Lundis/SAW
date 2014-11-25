# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_menuitem_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([('app_name', 'display_name', 'url')]),
        ),
    ]
