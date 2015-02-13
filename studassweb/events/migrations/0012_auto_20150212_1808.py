# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150212_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='signup_deadline',
            field=models.DateTimeField(verbose_name='Deadline for signups'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name='Event ends'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='stop',
            field=models.DateTimeField(verbose_name='Event starts'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='text',
            field=base.fields.ValidatedRichTextField(verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventitem',
            name='required',
            field=models.BooleanField(verbose_name='Is this field mandatory', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventitem',
            name='type',
            field=models.CharField(max_length=1, help_text='Decides what kind of data is allowed in this field', choices=[('B', 'Checkbox'), ('S', 'String'), ('T', 'Text'), ('I', 'Integer'), ('C', 'Choice')], verbose_name='Data type', default='I'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventsignup',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Full name'),
            preserve_default=True,
        ),
    ]
