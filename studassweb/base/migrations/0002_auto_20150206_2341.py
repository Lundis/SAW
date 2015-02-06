# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('url', models.CharField(max_length=300)),
                ('ip_address', models.IPAddressField()),
                ('type', models.CharField(choices=[('HELPTEXT', 'Help text feedback')], max_length=10)),
                ('response', models.CharField(choices=[('GOOD', 'Good'), ('BAD', 'Bad'), ('UNNE', 'Unnecessary')], max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='show_feedback_helptext',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
