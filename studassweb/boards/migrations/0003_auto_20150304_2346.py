# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20150304_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('is_setup', models.BooleanField(default=False,
                                                 help_text='Tells us if the first-time setup has been done')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='board',
            name='photo',
            field=models.ImageField(null=True, upload_to='boards/photos', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='boardmember',
            name='photo',
            field=models.ImageField(null=True, upload_to='boards/photos', blank=True),
            preserve_default=True,
        ),
    ]
