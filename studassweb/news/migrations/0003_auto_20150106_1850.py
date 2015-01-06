# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20141120_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_id',
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default='category', max_length=100),
            preserve_default=False,
        ),
    ]
