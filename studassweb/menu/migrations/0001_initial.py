# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('display_order', models.IntegerField()),
            ],
            options={
                'ordering': ['menu', 'display_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainMenuSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='menu/images', null=True)),
                ('inverted_style', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('menu_name', models.CharField(max_length=30, unique=True)),
                ('created_by', models.CharField(choices=[('AP', 'Created by app'), ('US', 'Created by user')], default='AP', max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('app_name', models.CharField(blank=True, max_length=50, null=True)),
                ('identifier', models.CharField(max_length=100, help_text='A unique identifier that is used to distinguish this item', unique=True)),
                ('display_name', models.CharField(max_length=30)),
                ('external_url', models.CharField(blank=True, max_length=200, null=True)),
                ('reverse_string', models.CharField(blank=True, max_length=100, null=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('created_by', models.CharField(choices=[('AP', 'Created by app'), ('US', 'Created by user')], default='AP', max_length=2)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
                ('submenu', models.ForeignKey(blank=True, null=True, to='menu.Menu')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('path', models.CharField(choices=[('simple', 'menu/menus/simple.html'), ('standard', 'menu/menus/simple.html')], default='standard', max_length=10, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(null=True)),
                ('uses_image', models.BooleanField(default=False)),
                ('preview', models.ImageField(upload_to='', null=True)),
                ('for_main_menu', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
