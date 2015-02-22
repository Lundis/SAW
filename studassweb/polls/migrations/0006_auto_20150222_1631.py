# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_votes_ip_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='description',
            field=base.fields.ValidatedRichTextField(max_length=300),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='votes',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
