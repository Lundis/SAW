# coding=utf-8
from django.contrib import admin
from .models import Menu, MenuTemplate, MenuItem, ItemInMenu, MainMenuSettings


admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(MenuTemplate)
admin.site.register(ItemInMenu)
admin.site.register(MainMenuSettings)
