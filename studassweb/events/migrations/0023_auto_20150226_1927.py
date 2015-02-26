# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20150223_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='send_email_for_reserves',
            field=models.BooleanField(default=True, verbose_name='Send email when someone is moved from reserve list to attending'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='use_captcha',
            field=models.BooleanField(default=False, verbose_name='Use captcha when anonymous people sign up'),
            preserve_default=True,
        ),
    ]
