# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('base', '0006_auto_20141204_1204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('_object_id', 'created')},
        ),
        migrations.AddField(
            model_name='comment',
            name='_content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='_object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(verbose_name='Date created', auto_now_add=True),
            preserve_default=True,
        ),
    ]
