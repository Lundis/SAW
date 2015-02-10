# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0007_auto_20150206_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='handled',
            field=models.BooleanField(default=False, verbose_name='Has this message been handled by someone?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='ordering_index',
            field=models.IntegerField(verbose_name='The position of this contact in the list of contacts'),
            preserve_default=True,
        ),
    ]
