# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    replaces = [('frontpage', '0001_initial'), ('frontpage', '0002_auto_20150212_1143'), ('frontpage', '0003_auto_20150212_1324'), ('frontpage', '0004_auto_20150302_1343')]

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrontPageItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('identifier', models.CharField(max_length=100)),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('location', models.CharField(choices=[('MB', 'Main bar'), ('SB', 'Side bar'), ('HD', 'Hidden')], max_length=2, default='HD')),
                ('ordering_index', models.IntegerField(validators=django.core.validators.MinValueValidator(1))),
                ('_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('_content_type', models.ForeignKey(to='contenttypes.ContentType', blank=True, null=True)),
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
        migrations.AlterUniqueTogether(
            name='frontpageitem',
            unique_together=set([('_content_type', '_object_id'), ('location', 'ordering_index')]),
        ),
        migrations.AlterField(
            model_name='frontpageitem',
            name='ordering_index',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='frontpageitem',
            name='module',
            field=models.CharField(max_length=50, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='frontpageitem',
            name='render_function',
            field=models.CharField(max_length=50, default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='frontpageitem',
            name='template',
            field=models.CharField(max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='frontpageitem',
            name='content',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
