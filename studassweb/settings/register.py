from menu.models import MenuItem
from users.models import SAWPermission

def get_menu_items():
    return [MenuItem.get_or_create("settings",
                                   "Settings",
                                   "/settings/",
                                   MenuItem.LOGIN_MENU,
                                   SAWPermission.get_or_create("can_view_settings"))]

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^settings/",)