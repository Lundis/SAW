# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sawpermission',
            name='permission',
            field=models.OneToOneField(to='auth.Permission'),
        ),
    ]
