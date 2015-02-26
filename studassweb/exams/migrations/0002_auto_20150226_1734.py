# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('ocr', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('exam_date', models.DateTimeField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exams.Course')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True)),
                ('examinator', models.ForeignKey(to='exams.Examinator', on_delete=django.db.models.deletion.PROTECT, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='singleexam',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='singleexam',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='singleexam',
            name='examinator',
        ),
        migrations.AlterField(
            model_name='examfile',
            name='exam_id',
            field=models.ForeignKey(to='exams.Exam'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='SingleExam',
        ),
    ]
