# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20141130_2300'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainMenuTemplateSettings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('image', models.ImageField(upload_to='menu/images', null=True)),
                ('chosen_tempalte', models.ForeignKey(to='menu.MenuTemplate')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='menutemplate',
            name='description',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menutemplate',
            name='name',
            field=models.CharField(max_length=100, unique=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menutemplate',
            name='preview',
            field=models.ImageField(upload_to='', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menutemplate',
            name='uses_image',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menutemplate',
            name='path',
            field=models.CharField(max_length=10, choices=[('simple', 'menu/menus/simple.html'), ('standard', 'menu/menus/simple.html'), ('large', 'menu/menus/large_menu.html')], unique=True, default='standard'),
            preserve_default=True,
        ),
    ]
