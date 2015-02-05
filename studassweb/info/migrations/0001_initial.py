# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoCategory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('permission', models.CharField(default='VIEW_PUBLIC', choices=[('VIEW_PUBLIC', 'can_view_public_info_pages'), ('VIEW_MEMBER', 'can_view_member_info_pages'), ('VIEW_BOARD', 'can_view_board_member_info_pages')], max_length=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfoPage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('text', ckeditor.fields.RichTextField()),
                ('permission', models.CharField(default='VIEW_PUBLIC', choices=[('VIEW_PUBLIC', 'can_view_public_info_pages'), ('VIEW_MEMBER', 'can_view_member_info_pages'), ('VIEW_BOARD', 'can_view_board_member_info_pages')], max_length=100)),
                ('category', models.ForeignKey(to='info.InfoCategory', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfoPageEdit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('date', models.DateTimeField(verbose_name='Date edited')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(to='info.InfoPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
