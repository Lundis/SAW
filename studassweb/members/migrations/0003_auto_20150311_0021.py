# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20150304_2255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('-date',)},
        ),
        migrations.AddField(
            model_name='payment',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 3, 10, 22, 21, 2, 365096, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='date_entered',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 3, 10, 22, 21, 4, 530371, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='expires',
            field=models.DateField(default=datetime.datetime(2015, 3, 10, 22, 21, 6, 319598, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
