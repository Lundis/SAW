# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('item', models.ForeignKey(to='menu.MenuItem')),
                ('menu', models.ForeignKey(to='menu.Menu')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='iteminmenu',
            unique_together=set([('menu', 'item')]),
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': ['display_order']},
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='auto_created',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='menu',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='visible',
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
    ]
