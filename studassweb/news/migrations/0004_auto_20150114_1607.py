# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20150112_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(to='news.Category', blank=True, through='news.ArticleInCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.TextField(blank=True, null=True, max_length=300),
            preserve_default=True,
        ),
    ]
