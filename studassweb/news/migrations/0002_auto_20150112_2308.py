# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.SlugField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=ckeditor.fields.RichTextField(),
            preserve_default=True,
        ),
    ]
