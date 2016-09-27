# coding=utf-8
from django.contrib import admin
from .models import InfoPage, InfoCategory, InfoPageEdit, PagesSettings

admin.site.register((InfoCategory,
                    InfoPage,
                    InfoPageEdit,
                    PagesSettings))
