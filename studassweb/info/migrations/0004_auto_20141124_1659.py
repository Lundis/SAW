# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_auto_20141124_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infopage',
            name='text_html',
        ),
        migrations.AlterField(
            model_name='infopage',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
