# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150601_2002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bootswatchtheme',
            name='preview_image',
        ),
        migrations.AddField(
            model_name='bootswatchtheme',
            name='preview_image_url',
            field=models.URLField(default='https://placehold.it/500x300'),
            preserve_default=False,
        ),
    ]
