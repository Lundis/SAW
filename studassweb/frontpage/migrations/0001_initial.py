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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('identifier', models.CharField(max_length=100)),
                ('title', models.TextField()),
                ('content', models.TextField(blank=True, null=True)),
                ('template', models.CharField(default='', max_length=200)),
                ('module', models.CharField(blank=True, default='', max_length=50)),
                ('render_function', models.CharField(blank=True, default='', max_length=50)),
                ('location', models.CharField(choices=[('MB', 'Main bar'), ('SB', 'Side bar'), ('HD', 'Hidden')],
                                              default='HD', max_length=2)),
                ('ordering_index', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('_content_type', models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('ordering_index',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='frontpageitem',
            unique_together={('location', 'ordering_index'), ('_content_type', '_object_id')},
        ),
    ]
