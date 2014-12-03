# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_auto_20141202_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainMenuSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='menu/images')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='mainmenutemplatesettings',
            name='chosen_tempalte',
        ),
        migrations.DeleteModel(
            name='MainMenuTemplateSettings',
        ),
        migrations.AddField(
            model_name='menutemplate',
            name='for_main_menu',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
