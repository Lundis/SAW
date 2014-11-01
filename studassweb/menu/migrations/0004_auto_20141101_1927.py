# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20141101_1902'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='iteminmenu',
            unique_together=set([('menu', 'item')]),
        ),
    ]
