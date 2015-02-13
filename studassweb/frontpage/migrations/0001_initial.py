# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrontPageItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('identifier', models.CharField(max_length=100)),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('location', models.CharField(choices=[('MB', 'Main bar'), ('SB', 'Side bar'), ('HD', 'Hidden')], max_length=2, default='HD')),
                ('ordering_index', models.IntegerField(validators=django.core.validators.MinValueValidator(1))),
                ('_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('_content_type', models.ForeignKey(null=True, to='contenttypes.ContentType', blank=True)),
            ],
            options={
                'ordering': ('ordering_index',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='frontpageitem',
            unique_together=set([('location', 'ordering_index')]),
        ),
    ]
