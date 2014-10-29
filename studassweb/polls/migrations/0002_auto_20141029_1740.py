# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300)),
                ('publication', models.DateTimeField(verbose_name='Date published')),
                ('expiration', models.DateTimeField(verbose_name='Poll closes')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('choice_id', models.ForeignKey(to='polls.Choice')),
                ('members_choice', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='user_choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Poll_question',
        ),
        migrations.DeleteModel(
            name='User_choice',
        ),
        migrations.AddField(
            model_name='choice',
            name='id_to_poll',
            field=models.ForeignKey(to='polls.Poll'),
            preserve_default=True,
        ),
    ]
