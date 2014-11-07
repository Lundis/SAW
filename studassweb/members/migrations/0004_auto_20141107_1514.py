# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20141107_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentpurpose',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
