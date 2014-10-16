# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll_question',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('question_text', models.CharField(max_length=300)),
                ('publication_date', models.DateTimeField(verbose_name='Date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_choice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('choice_text', models.CharField(max_length=300)),
                ('vote_amount', models.IntegerField(default=0)),
                ('question', models.ForeignKey(to='polls.Poll_question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
