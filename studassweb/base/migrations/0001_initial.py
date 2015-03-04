# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BootswatchTheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('theme_path', models.CharField(max_length=200)),
                ('preview_image', models.ImageField(upload_to='base/bootswatch')),
                ('preview_url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('text', models.TextField(max_length=400)),
                ('created', models.DateTimeField(verbose_name='Date created', auto_now_add=True)),
                ('_object_id', models.PositiveIntegerField()),
                ('_content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('_object_id', 'created'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DisabledModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('app_name', models.CharField(max_length=50, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=300)),
                ('ip_address', models.IPAddressField()),
                ('type', models.CharField(choices=[('HELPTEXT', 'Help text feedback')], max_length=10)),
                ('response', models.CharField(choices=[('GOOD', 'Good'), ('BAD', 'Bad'), ('UNNE', 'Unnecessary')], max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('association_name', models.CharField(default='Site name', max_length=100)),
                ('base_url', models.CharField(default='http://localhost:8000', max_length=150)),
                ('association_contact_email', models.EmailField(default='example@example.com', max_length=254)),
                ('association_founded', models.IntegerField(default=1900)),
                ('bootstrap_theme_url', models.CharField(default='css/themes/bootstrap.min.css', max_length=200)),
                ('bootstrap_theme_mod_url', models.CharField(blank=True, default='css/themes/bootstrap-theme.min.css', max_length=200, null=True)),
                ('bootswatch_version', models.CharField(default=None, max_length=50, null=True)),
                ('bootswatch_last_checked', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0))),
                ('show_feedback_helptext', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set([('type', 'user', 'url', 'ip_address'), ('type', 'user', 'url')]),
        ),
    ]
