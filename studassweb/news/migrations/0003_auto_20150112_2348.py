# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20150112_2308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-created_date', '-created_time']},
        ),
        migrations.RemoveField(
            model_name='article',
            name='created',
        ),
        migrations.AddField(
            model_name='article',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 1, 12, 21, 48, 23, 358802, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='created_time',
            field=models.TimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 12, 21, 48, 34, 365431, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.TextField(blank=True, max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together=set([('slug', 'created_date')]),
        ),
    ]
