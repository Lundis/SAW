# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_album_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='album_id',
            new_name='album',
        ),
    ]
