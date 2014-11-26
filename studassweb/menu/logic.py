from base.utils import get_modules_with, get_function_from_module
from base.models import DisabledModule


def get_all_menu_items():
    """
    Returns a list of all available menu items.
    """
    modules = get_modules_with("register", "get_menu_items")
    items = [[], [], []]
    for module, menu_items_func in modules:
        if DisabledModule.is_enabled(module):
            menu_items = menu_items_func()
            if menu_items[0]:
                items[0] += menu_items[0]
            if menu_items[1]:
                items[1] += menu_items[1]
            if menu_items[2]:
                items[2] += menu_items[2]
    return items