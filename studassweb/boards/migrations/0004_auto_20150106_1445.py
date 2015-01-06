# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_auto_20150106_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='board',
            new_name='boardtype',
        ),
        migrations.AlterField(
            model_name='board',
            name='photo',
            field=models.ImageField(upload_to='boards/photos', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='boardmember',
            name='photo',
            field=models.ImageField(upload_to='boards/photos', blank=True),
            preserve_default=True,
        ),
    ]
