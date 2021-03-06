# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_article_search_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='permission',
            field=models.CharField(choices=[('can_view_public_news', 'Visible for everyone'), ('can_view_member_news', 'Visible for members'), ('can_view_board_member_news', 'Visible for board members')], default='VIEW_PUBLIC', max_length=100),
        ),
        migrations.AddField(
            model_name='newssettings',
            name='number_of_articles_on_frontpage',
            field=models.IntegerField(default=5),
        ),
    ]
