# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20150111_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customentry',
            name='content',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customfield',
            name='name',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(unique=True, blank=True, null=True, max_length=75),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='enrollment_year',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='user_ext',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='users.UserExtension', blank=True, unique=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='customentry',
            unique_together=set([('field', 'member')]),
        ),
    ]
