# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20150216_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='album_id',
            field=models.ForeignKey(to='gallery.Album'),
            preserve_default=True,
        ),
    ]
