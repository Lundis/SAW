# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiuploader.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MultiuploaderFile',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField()),
                ('file', models.FileField(upload_to=multiuploader.models.MultiuploaderFile._upload_to, max_length=255)),
            ],
            options={
                'verbose_name': 'multiuploader file',
                'verbose_name_plural': 'multiuploader files',
            },
            bases=(models.Model,),
        ),
    ]
