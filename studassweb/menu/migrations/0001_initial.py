# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('menu_name', models.CharField(max_length=30, unique=True)),
                ('template', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('app_name', models.CharField(max_length=30)),
                ('display_name', models.CharField(max_length=30)),
                ('display_order', models.IntegerField()),
                ('visible', models.BooleanField(default=True)),
                ('url', models.CharField(max_length=100)),
                ('auto_created', models.BooleanField(default=False)),
                ('menu', models.ForeignKey(to='menu.Menu')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
