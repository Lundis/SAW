# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import base.fields
import django.core.validators
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('contact', '0001_initial'), ('contact', '0002_settings'), ('contact', '0003_auto_20150202_1147'), ('contact', '0004_auto_20150204_1240'), ('contact', '0005_auto_20150204_1425'), ('contact', '0006_contactsettings'), ('contact', '0007_auto_20150206_2154'), ('contact', '0008_auto_20150210_1525'), ('contact', '0009_auto_20150210_1715'), ('contact', '0010_auto_20150211_0038')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=500)),
                ('from_email', models.EmailField(max_length=75)),
                ('date_and_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('from_person', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('info_text', ckeditor.fields.RichTextField()),
                ('save_to_db', models.BooleanField(default=True)),
                ('send_email', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='contact',
            field=models.ForeignKey(to='contact.ContactInfo', default=1),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='contactinfo',
            options={'ordering': ('ordering_index',)},
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='ordering_index',
            field=models.IntegerField(verbose_name='The position of this contact in the list of contacts', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ContactSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('_is_setup', models.BooleanField(help_text='Tells us if the first-time setup has been done', default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='info_text',
            field=ckeditor.fields.RichTextField(verbose_name='Contact details text'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='name',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='save_to_db',
            field=models.BooleanField(verbose_name='Should the message be saved to the database?', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='send_email',
            field=models.BooleanField(verbose_name='Should the message be sent to the specified email?', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='from_email',
            field=models.EmailField(verbose_name='Your email', max_length=75),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(verbose_name='Message', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='title',
            field=models.CharField(verbose_name='Subject', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='handled',
            field=models.BooleanField(verbose_name='Has this message been handled by someone?', default=False),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-date_and_time',)},
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='info_text',
            field=base.fields.ValidatedRichTextField(verbose_name='Contact details text'),
            preserve_default=True,
        ),
    ]
