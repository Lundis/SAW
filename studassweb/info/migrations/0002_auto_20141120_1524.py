# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_menuitem_submenu'),
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('submenu', models.ForeignKey(to='menu.Menu')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='infopage',
            name='text_html',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='infopage',
            name='text',
            field=models.TextField(),
        ),
    ]
