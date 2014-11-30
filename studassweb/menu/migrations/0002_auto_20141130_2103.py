# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='iteminmenu',
            unique_together=set([('menu', 'item'), ('menu', 'item', 'display_order')]),
        ),
    ]
