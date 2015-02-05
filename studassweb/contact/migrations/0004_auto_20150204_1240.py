# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20150202_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
        migrations.DeleteModel(
            name='Settings',
        ),
        migrations.AddField(
            model_name='message',
            name='contact',
            field=models.ForeignKey(default=1, to='contact.ContactInfo'),
            preserve_default=False,
        ),
    ]
