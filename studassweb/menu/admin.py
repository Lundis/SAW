from django.contrib import admin
from .models import Menu, MenuTemplate, MenuItem, ItemInMenu


admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(MenuTemplate)
admin.site.register(ItemInMenu)
