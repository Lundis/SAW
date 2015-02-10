# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20150210_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infopage',
            name='text',
            field=base.fields.ValidatedRichTextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='infopageedit',
            name='text',
            field=base.fields.ValidatedRichTextField(),
            preserve_default=True,
        ),
    ]
