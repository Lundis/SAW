# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0002_auto_20141116_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleexam',
            name='image',
            field=models.ImageField(upload_to='exams_files'),
        ),
    ]
