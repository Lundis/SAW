# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20141201_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userextension',
            name='member',
        ),
        migrations.AddField(
            model_name='userextension',
            name='can_apply_for_membership',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userextension',
            name='email_verification_code',
            field=models.CharField(unique=True, max_length=32, default='3jjrdmtu59rpduj1p6ah7bmeam64ibu4'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userextension',
            name='email_verified',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
