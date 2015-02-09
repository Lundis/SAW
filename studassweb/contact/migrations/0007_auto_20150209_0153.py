# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_contactsettings'),
    ]

    operations = [
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
            name='ordering_index',
            field=models.IntegerField(verbose_name='The position of this contact in the list of contacts', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='save_to_db',
            field=models.BooleanField(default=True, verbose_name='Should the message be saved to the database?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='send_email',
            field=models.BooleanField(default=True, verbose_name='Should the message be sent to the specified email?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactsettings',
            name='_is_setup',
            field=models.BooleanField(default=False, help_text='Tells us if the first-time setup has been done'),
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
    ]
