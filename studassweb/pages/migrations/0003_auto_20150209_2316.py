# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20150209_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infopage',
            name='category',
            field=models.ForeignKey(to='pages.InfoCategory', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='infopage',
            name='for_frontpage',
            field=models.BooleanField(help_text='Is this meant to be shown on the front page?', default=False),
            preserve_default=True,
        ),
    ]
