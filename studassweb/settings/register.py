from menu.models import MenuItem

def get_menu_items():
    return [MenuItem.get_or_create("settings", "Settings", "/settings/")]

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^settings/",)