# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_sawpermission_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='sawpermission',
            name='id',
            field=models.AutoField(primary_key=True, default=None, verbose_name='ID', auto_created=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sawpermission',
            name='permission',
            field=models.ForeignKey(unique=True, to='auth.Permission'),
            preserve_default=True,
        ),
    ]
