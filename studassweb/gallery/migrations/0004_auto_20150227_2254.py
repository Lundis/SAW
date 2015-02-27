# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20150222_2351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photofile',
            name='photo_id',
        ),
        migrations.DeleteModel(
            name='PhotoFile',
        ),
        migrations.AddField(
            model_name='photo',
            name='image',
            field=models.ImageField(default='', upload_to='gallery_files'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photo',
            name='uploaded',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
