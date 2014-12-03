# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20141130_2103'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='iteminmenu',
            unique_together=set([('menu', 'display_order'), ('menu', 'item')]),
        ),
    ]
