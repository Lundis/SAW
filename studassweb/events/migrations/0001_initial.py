# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=500)),
                ('start', models.DateTimeField()),
                ('stop', models.DateTimeField()),
                ('signup_deadline', models.DateTimeField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventSignup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=75)),
                ('matricle', models.CharField(max_length=20)),
                ('association', models.CharField(max_length=200)),
                ('diet', models.CharField(max_length=200)),
                ('other', models.CharField(max_length=200)),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemInEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('event', models.ForeignKey(to='events.Event')),
                ('item', models.ForeignKey(to='events.EventItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemInSignup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('item', models.ForeignKey(to='events.EventItem')),
                ('signup', models.ForeignKey(to='events.EventSignup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
