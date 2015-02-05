# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='info_text',
            field=ckeditor.fields.RichTextField(),
            preserve_default=True,
        ),
    ]
