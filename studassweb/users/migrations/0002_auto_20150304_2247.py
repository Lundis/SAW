# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_squashed_0007_auto_20150304_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sawpermission',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sawpermission',
            name='module',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
