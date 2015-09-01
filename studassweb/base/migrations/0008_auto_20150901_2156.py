# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_cssmap_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cssoverridecontent',
            name='description',
        ),
        migrations.AddField(
            model_name='cssoverridefile',
            name='description',
            field=models.TextField(default='', max_length=200),
        ),
    ]
