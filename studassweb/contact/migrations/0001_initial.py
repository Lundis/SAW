# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django.core.validators
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('info_text', base.fields.ValidatedRichTextField(verbose_name='Contact details text')),
                ('save_to_db', models.BooleanField(verbose_name='Should the message be saved to the database?',
                                                   default=True)),
                ('send_email', models.BooleanField(verbose_name='Should the message be sent to the specified email?',
                                                   default=True)),
                ('email', models.EmailField(max_length=75)),
                ('ordering_index', models.IntegerField(
                    validators=[django.core.validators.MinValueValidator(1)],
                    verbose_name='The position of this contact in the list of contacts')),
            ],
            options={
                'ordering': ('ordering_index',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('_is_setup', models.BooleanField(default=False,
                                                  help_text='Tells us if the first-time setup has been done')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='Subject', max_length=100)),
                ('message', models.TextField(verbose_name='Message', max_length=500)),
                ('from_email', models.EmailField(verbose_name='Your email', max_length=75)),
                ('date_and_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('handled', models.BooleanField(verbose_name='Has this message been handled by someone?',
                                                default=False)),
                ('contact', models.ForeignKey(to='contact.ContactInfo')),
                ('from_person', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_and_time',),
            },
            bases=(models.Model,),
        ),
    ]
