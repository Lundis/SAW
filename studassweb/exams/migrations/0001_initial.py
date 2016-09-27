# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL,
                                                 null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('ocr', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('exam_date', models.DateTimeField()),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exams.Course')),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL,
                                                 null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExamFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='exams_files')),
                ('exam_id', models.ForeignKey(to='exams.Exam')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Examinator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL,
                                                 null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='exam',
            name='examinator',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, null=True,
                                    to='exams.Examinator'),
            preserve_default=True,
        ),
    ]
