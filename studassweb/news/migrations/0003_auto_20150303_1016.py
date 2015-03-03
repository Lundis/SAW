# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20150211_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsSettings',
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
            model_name='article',
            name='picture',
            field=models.ImageField(null=True, help_text='A small picture used in the news feed', upload_to='news/article_thumbnails', blank=True),
            preserve_default=True,
        ),
    ]
