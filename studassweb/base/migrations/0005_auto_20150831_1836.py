# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0004_auto_20150826_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSSOverrideContent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('description', models.TextField(max_length=200)),
                ('css', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CSSOverrideFile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='cssoverridecontent',
            name='file',
            field=models.ForeignKey(to='base.CSSOverrideFile'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='current_css_override',
            field=models.ForeignKey(default=None, to='base.CSSOverrideContent', null=True),
        ),
    ]
