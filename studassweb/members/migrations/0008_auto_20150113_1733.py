# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_auto_20150112_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(null=True, max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('first_name', 'last_name', 'email')]),
        ),
    ]
