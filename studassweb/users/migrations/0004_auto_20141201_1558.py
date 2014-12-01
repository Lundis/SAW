# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20141201_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextension',
            name='email_verification_code',
            field=models.CharField(unique=True, max_length=32, default='dov8ipddgs6zvq8m0vvgor0ic5ti5aw8'),
            preserve_default=True,
        ),
    ]
