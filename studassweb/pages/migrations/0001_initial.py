# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menu', '0003_mainmenusettings_inverted_style'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('permission', models.CharField(default='VIEW_PUBLIC', choices=[('VIEW_PUBLIC', 'can_view_public_info_pages'), ('VIEW_MEMBER', 'can_view_member_info_pages'), ('VIEW_BOARD', 'can_view_board_member_info_pages')], max_length=15)),
                ('menu_item', models.ForeignKey(to='menu.MenuItem', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfoPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('text', ckeditor.fields.RichTextField()),
                ('permission', models.CharField(default='VIEW_PUBLIC', choices=[('VIEW_PUBLIC', 'can_view_public_info_pages'), ('VIEW_MEMBER', 'can_view_member_info_pages'), ('VIEW_BOARD', 'can_view_board_member_info_pages')], max_length=100)),
                ('for_frontpage', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='pages.InfoCategory', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfoPageEdit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('date', models.DateTimeField(verbose_name='Date edited')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(to='pages.InfoPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
