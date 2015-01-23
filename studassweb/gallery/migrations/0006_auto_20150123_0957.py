# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20150112_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoFile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('image', models.ImageField(upload_to='gallery_files')),
                ('photo_id', models.ForeignKey(to='gallery.Photo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='photo',
            name='image',
        ),
        migrations.AlterField(
            model_name='photo',
            name='album_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gallery.Album'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
