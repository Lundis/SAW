from menu.models import Menu, MenuTemplate
from base.utils import get_modules_with
from base.models import DisabledModule

def setup_settings():
    setup_settings_menu()

def setup_settings_menu():
    template, created = MenuTemplate.objects.get_or_create(path="settings/menu.html")

    menu, created = Menu.objects.get_or_create(menu_name="settings_menu", template=template)
    # TODO: add menu items for all enabled modules that have a settings page
    settings_items_funcs = get_modules_with("register", "get_settings_items")
    for module, func in settings_items_funcs:
        if DisabledModule.is_enabled(module):
            settings_items = func()
            for item in settings_items:
                # TODO: fix the ordering somehow
                menu.add_item(item, 0)