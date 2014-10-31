# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20141021_0050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='iteminmenu',
            options={'ordering': ['display_order']},
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={},
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='display_order',
        ),
        migrations.AddField(
            model_name='iteminmenu',
            name='display_order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([('app_name', 'display_name', 'url')]),
        ),
    ]
