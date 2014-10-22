# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20141021_0050'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='disabled_module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('app_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='main_menu',
            field=models.ForeignKey(to='menu.Menu', null=True, blank=True),
            preserve_default=True,
        ),
    ]
