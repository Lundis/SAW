from base.utils import get_modules_with, get_function_from_module
from base.models import DisabledModule

def get_all_menu_items():
    """
    Returns a list of all available menu items.
    """
    modules = get_modules_with("register", "get_menu_items")
    items = []
    for module in modules:
        if DisabledModule.is_enabled(module):
            menu_items_func = get_function_from_module(module, "register", "get_menu_items")
            menu_items = menu_items_func()
            if menu_items:
                items += menu_items
    return items