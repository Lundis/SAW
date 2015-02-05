# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_auto_20150204_1240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactinfo',
            options={'ordering': ('ordering_index',)},
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='ordering_index',
            field=models.IntegerField(unique=True, default=0),
            preserve_default=False,
        ),
    ]
