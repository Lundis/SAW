# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0004_auto_20141117_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleexam',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exams.Course'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='singleexam',
            name='examinator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exams.Examinator'),
            preserve_default=True,
        ),
    ]
