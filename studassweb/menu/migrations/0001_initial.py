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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('image', models.ImageField(null=True, upload_to='menu/images', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('menu_name', models.CharField(max_length=30, unique=True)),
                ('created_by', models.CharField(default='AP', choices=[('AP', 'Created by app'), ('US', 'Created by user')], max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('app_name', models.CharField(max_length=50, null=True, blank=True)),
                ('display_name', models.CharField(max_length=30)),
                ('external_url', models.CharField(max_length=200, null=True, blank=True)),
                ('reverse_string', models.CharField(max_length=100, null=True, blank=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('created_by', models.CharField(default='AP',
                                                choices=[('AP', 'Created by app'), ('US', 'Created by user')],
                                                max_length=2)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
                ('submenu', models.ForeignKey(to='menu.Menu', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuTemplate',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('path', models.CharField(default='standard', choices=[('simple', 'menu/menus/simple.html'), ('standard', 'menu/menus/simple.html')], max_length=10, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(null=True)),
                ('uses_image', models.BooleanField(default=False)),
                ('preview', models.ImageField(null=True, upload_to='')),
                ('for_main_menu', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
