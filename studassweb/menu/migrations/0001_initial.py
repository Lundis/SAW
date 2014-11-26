# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('menu_name', models.CharField(unique=True, max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('app_name', models.CharField(max_length=50, null=True, blank=True)),
                ('display_name', models.CharField(max_length=30)),
                ('external_url', models.URLField(null=True, blank=True)),
                ('reverse_string', models.CharField(max_length=100, null=True, blank=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('type', models.CharField(max_length=2, choices=[('AP', 'Created by app'), ('US', 'Created by user')], default='AP')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
                ('submenu', models.ForeignKey(to='menu.Menu', null=True)),
                ('view_permission', models.ForeignKey(null=True, blank=True, to='users.SAWPermission')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([('app_name', 'display_name')]),
        ),
        migrations.AddField(
            model_name='menu',
            name='template',
            field=models.ForeignKey(null=True, blank=True, to='menu.MenuTemplate'),
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
