# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='frontpageitem',
            unique_together=set([('location', 'ordering_index'), ('_content_type', '_object_id')]),
        ),
    ]
