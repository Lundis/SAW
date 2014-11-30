# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boardmember',
            old_name='person_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='board',
            name='photo',
            field=models.ImageField(upload_to='association/photos'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='boardmember',
            name='photo',
            field=models.ImageField(upload_to='association/photos'),
            preserve_default=True,
        ),
    ]
