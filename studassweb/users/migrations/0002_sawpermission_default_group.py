# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sawpermission',
            name='default_group',
            field=models.ForeignKey(default=None, to='auth.Group', null=True),
            preserve_default=True,
        ),
    ]
