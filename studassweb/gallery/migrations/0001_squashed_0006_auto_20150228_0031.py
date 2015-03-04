# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('gallery', '0001_initial'), ('gallery', '0002_auto_20150216_2117'), ('gallery', '0003_auto_20150222_2351'), ('gallery', '0004_auto_20150227_2254'), ('gallery', '0005_album_slug'), ('gallery', '0006_auto_20150228_0031')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('description', models.TextField(max_length=300)),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(to='gallery.Album')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True)),
                ('image', models.ImageField(default='', upload_to='gallery_files')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='album',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
    ]
