# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='infopageedit',
            options={'ordering': ('-date',)},
        ),
        migrations.AddField(
            model_name='infopage',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='infopageedit',
            name='text',
            field=ckeditor.fields.RichTextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='infopageedit',
            name='date',
            field=models.DateTimeField(verbose_name='Date edited', auto_now_add=True),
            preserve_default=True,
        ),
    ]
