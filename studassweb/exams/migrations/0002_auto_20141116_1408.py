# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='singleexam',
            name='photo_id',
        ),
        migrations.AddField(
            model_name='singleexam',
            name='image',
            field=models.ImageField(default='', blank=True, upload_to='exams_files'),
            preserve_default=False,
        ),
    ]
