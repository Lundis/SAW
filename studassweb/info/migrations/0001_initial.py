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
            name='InfoPage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfoPageEdit',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date', models.DateTimeField(verbose_name='Date edited')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(to='info.InfoPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
