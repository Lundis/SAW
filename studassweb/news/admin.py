# coding=utf-8
from django.contrib import admin
from .models import Article, Category, NewsSettings


admin.site.register((Article,
                     Category,
                     NewsSettings))
