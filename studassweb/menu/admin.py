from django.contrib import admin
from .models import Menu, MenuTemplate, MenuItem, ItemInMenu, MainMenuSettings
from solo.admin import SingletonModelAdmin


admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(MenuTemplate)
admin.site.register(ItemInMenu)
admin.site.register(MainMenuSettings)