# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0005_auto_20141126_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleexam',
            name='examinator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, null=True, to='exams.Examinator', blank=True),
            preserve_default=True,
        ),
    ]
