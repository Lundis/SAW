# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='view_permission',
            field=models.ForeignKey(blank=True, null=True, to='users.SAWPermission'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([('display_name', 'url')]),
        ),
        migrations.AddField(
            model_name='menu',
            name='template',
            field=models.ForeignKey(blank=True, null=True, to='menu.MenuTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='iteminmenu',
            name='item',
            field=models.ForeignKey(to='menu.MenuItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='iteminmenu',
            name='menu',
            field=models.ForeignKey(to='menu.Menu'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='iteminmenu',
            unique_together=set([('menu', 'item')]),
        ),
    ]
