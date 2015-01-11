# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20141201_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customentry',
            name='field',
            field=models.ForeignKey(to='members.CustomField'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customentry',
            name='member',
            field=models.ForeignKey(to='members.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='applying',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='email',
            field=models.EmailField(unique=True, default='a@a.com', max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='first_name',
            field=models.CharField(default='first name', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='last_name',
            field=models.CharField(default='last name', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='graduation_year',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
