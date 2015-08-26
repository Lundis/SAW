# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20150826_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bootswatchtheme',
            name='theme_path',
        ),
        migrations.AddField(
            model_name='bootswatchtheme',
            name='bs_css_url',
            field=models.URLField(default='css/themes/bootstrap.min.css'),
            preserve_default=False,
        ),
    ]
