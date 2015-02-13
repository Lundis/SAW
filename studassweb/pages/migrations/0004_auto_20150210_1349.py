# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150209_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='infocategory',
            name='slug',
            field=models.SlugField(editable=False, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='infopage',
            name='slug',
            field=models.SlugField(editable=False, default=''),
            preserve_default=False,
        ),
    ]
