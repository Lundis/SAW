# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0009_auto_20150210_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfo',
            name='info_text',
            field=base.fields.ValidatedRichTextField(verbose_name='Contact details text'),
            preserve_default=True,
        ),
    ]
