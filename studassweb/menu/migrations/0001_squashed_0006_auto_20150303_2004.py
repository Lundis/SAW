# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_default_identifiers(apps, schema_editor):
    print(apps)
    MenuItem = apps.get_model("menu", "menuitem")
    db_alias = schema_editor.connection.alias
    items = MenuItem.objects.using(db_alias).all()
    for item in items:
        item.identifier = item.app_name + "_" + item.display_name
        item.save()

class Migration(migrations.Migration):

    replaces = [('menu', '0001_initial'), ('menu', '0002_auto_20150128_1119'), ('menu', '0003_mainmenusettings_inverted_style'), ('menu', '0004_menu_item_identifier'), ('menu', '0005_auto_20150215_1847'), ('menu', '0006_auto_20150303_2004')]

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInMenu',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('display_order', models.IntegerField()),
            ],
            options={
                'ordering': ['menu', 'display_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MainMenuSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='menu/images')),
                ('inverted_style', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('menu_name', models.CharField(unique=True, max_length=30)),
                ('created_by', models.CharField(default='AP', max_length=2, choices=[('AP', 'Created by app'), ('US', 'Created by user')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('app_name', models.CharField(blank=True, null=True, max_length=50)),
                ('display_name', models.CharField(max_length=30)),
                ('external_url', models.CharField(blank=True, null=True, max_length=200)),
                ('reverse_string', models.CharField(blank=True, null=True, max_length=100)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('created_by', models.CharField(default='AP', max_length=2, choices=[('AP', 'Created by app'), ('US', 'Created by user')])),
                ('content_type', models.ForeignKey(null=True, to='contenttypes.ContentType')),
                ('submenu', models.ForeignKey(null=True, to='menu.Menu')),
                ('view_permission', models.ForeignKey(to='users.SAWPermission', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('path', models.CharField(unique=True, default='standard', max_length=10, choices=[('simple', 'menu/menus/simple.html'), ('standard', 'menu/menus/simple.html')])),
                ('name', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField(null=True)),
                ('uses_image', models.BooleanField(default=False)),
                ('preview', models.ImageField(upload_to='', null=True)),
                ('for_main_menu', models.BooleanField(default=False)),
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
            field=models.ForeignKey(to='menu.MenuTemplate', blank=True, null=True),
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
            unique_together=set([('menu', 'item'), ('menu', 'display_order')]),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='identifier',
            field=models.CharField(unique=True, default=None, null=True, max_length=100),
            preserve_default=True,
        ),
        migrations.RunPython(
            code=set_default_identifiers,
            reverse_code=None,
            atomic=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='identifier',
            field=models.CharField(unique=True, default=None, null=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([]),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='identifier',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='identifier',
            field=models.CharField(unique=True, help_text='A unique identifier that is used to distinguish this item', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='submenu',
            field=models.ForeignKey(to='menu.Menu', blank=True, null=True),
            preserve_default=True,
        ),
    ]
