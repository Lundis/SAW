# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0008_auto_20150210_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-date_and_time',)},
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='ordering_index',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='The position of this contact in the list of contacts'),
            preserve_default=True,
        ),
    ]
