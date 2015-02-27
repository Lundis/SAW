# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20150215_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagesSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('is_setup', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='infocategory',
            name='permission',
            field=models.CharField(max_length=100, default='VIEW_PUBLIC', choices=[('can_view_public_info_pages', 'Visible for everyone'), ('can_view_member_info_pages', 'Visible for members'), ('can_view_board_member_info_pages', 'Visible for board members')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='infopage',
            name='permission',
            field=models.CharField(max_length=100, default='VIEW_PUBLIC', choices=[('can_view_public_info_pages', 'Visible for everyone'), ('can_view_member_info_pages', 'Visible for members'), ('can_view_board_member_info_pages', 'Visible for board members')]),
            preserve_default=True,
        ),
    ]
