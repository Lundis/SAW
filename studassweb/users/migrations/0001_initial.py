# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0004_auto_20141107_1514'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DummyPermissionBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LdapLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('hostname', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=50)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SAWPermission',
            fields=[
                ('permission', models.ForeignKey(serialize=False, to='auth.Permission', primary_key=True)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('description', models.TextField(default='', max_length=1000, blank=True)),
                ('link_to_homepage', models.URLField(default='', blank=True)),
                ('member', models.ForeignKey(unique=True, null=True, blank=True, to='members.Member')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
