# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150206_2341'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set([('user', 'url'), ('user', 'url', 'ip_address')]),
        ),
    ]
