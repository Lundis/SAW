# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20150114_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='association_contact_email',
            field=models.EmailField(default='example@example.com', max_length=254),
            preserve_default=True,
        ),
    ]
