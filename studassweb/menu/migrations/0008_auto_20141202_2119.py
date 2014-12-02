# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_auto_20141202_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainmenusettings',
            name='image',
            field=models.ImageField(upload_to='menu/images', blank=True, null=True),
            preserve_default=True,
        ),
    ]
