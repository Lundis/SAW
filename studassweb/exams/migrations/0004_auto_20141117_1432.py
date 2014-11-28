# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_auto_20141116_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamFile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('image', models.ImageField(upload_to='exams_files')),
                ('exam_id', models.ForeignKey(to='exams.SingleExam')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='singleexam',
            name='image',
        ),
        migrations.AlterField(
            model_name='singleexam',
            name='ocr',
            field=models.TextField(blank=True),
        ),
    ]
