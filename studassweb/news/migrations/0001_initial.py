# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('summary', models.TextField(null=True, blank=True, max_length=300)),
                ('slug', models.SlugField(editable=False)),
                ('text', ckeditor.fields.RichTextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('created_time', models.TimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('picture', models.ImageField(null=True, blank=True, upload_to='news/article_thumbnails')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date', '-created_time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(blank=True, to='news.Category'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together=set([('slug', 'created_date')]),
        ),
    ]
