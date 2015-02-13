# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20150211_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iteminsignup',
            name='amount',
        ),
    ]
