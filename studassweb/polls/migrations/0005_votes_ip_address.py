# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20150202_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='votes',
            name='ip_address',
            field=models.IPAddressField(default=None),
            preserve_default=True,
        ),
    ]
