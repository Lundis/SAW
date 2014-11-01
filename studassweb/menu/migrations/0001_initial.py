# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('display_order', models.IntegerField()),
            ],
            options={
                'ordering': ['menu', 'display_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('menu_name', models.CharField(unique=True, max_length=30)),
                ('template', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('app_name', models.CharField(blank=True, max_length=50, null=True)),
                ('display_name', models.CharField(max_length=30)),
                ('url', models.URLField()),
                ('default_menu', models.CharField(max_length=2, choices=[('MM', 'Main menu'), ('LM', 'Login menu'), ('NO', 'No menu')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([('display_name', 'url')]),
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
            unique_together=set([('menu', 'display_order'), ('menu', 'item')]),
        ),
    ]
