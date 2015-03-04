# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_userextension_incomplete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kerberosserver',
            name='realm',
            field=models.CharField(help_text='Example: SRV.DOMAIN.COM', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kerberosserver',
            name='service',
            field=models.CharField(help_text='Example: krbtgt@SRV.DOMAIN.COM', max_length=255),
            preserve_default=True,
        ),
    ]
