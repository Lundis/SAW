# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
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
            name='Menu',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('menu_name', models.CharField(max_length=30, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('app_name', models.CharField(null=True, blank=True, max_length=50)),
                ('display_name', models.CharField(max_length=30)),
                ('url', models.URLField()),
                ('default_menu', models.CharField(choices=[('MM', 'Main menu'), ('LM', 'Login menu'), ('NO', 'No menu')], max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuTemplate',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('path', models.CharField(max_length=100, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
