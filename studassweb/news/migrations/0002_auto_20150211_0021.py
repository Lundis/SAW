# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=base.fields.ValidatedRichTextField(),
            preserve_default=True,
        ),
    ]
