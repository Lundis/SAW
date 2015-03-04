# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(editable=False)),
                ('permission', models.CharField(choices=[('can_view_public_info_pages', 'Visible for everyone'), ('can_view_member_info_pages', 'Visible for members'), ('can_view_board_member_info_pages', 'Visible for board members')], default='VIEW_PUBLIC', max_length=100)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='menu.MenuItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfoPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(editable=False)),
                ('text', base.fields.ValidatedRichTextField()),
                ('permission', models.CharField(choices=[('can_view_public_info_pages', 'Visible for everyone'), ('can_view_member_info_pages', 'Visible for members'), ('can_view_board_member_info_pages', 'Visible for board members')], default='VIEW_PUBLIC', max_length=100)),
                ('for_frontpage', models.BooleanField(default=False, help_text='Is this meant to be shown on the front page?')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, to='pages.InfoCategory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InfoPageEdit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('text', base.fields.ValidatedRichTextField()),
                ('date', models.DateTimeField(verbose_name='Date edited', auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(to='pages.InfoPage')),
            ],
            options={
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PagesSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('is_setup', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
