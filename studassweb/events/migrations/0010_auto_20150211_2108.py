# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150211_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='text',
            field=base.fields.ValidatedRichTextField(),
            preserve_default=True,
        ),
    ]
