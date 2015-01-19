# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20150106_1445'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='boardmember',
            unique_together=set([('board', 'role', 'member')]),
        ),
    ]
