from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import WEBMASTER

def get_menu_items():
    return [MenuItem.get_or_create("install",
                                   "Install",
                                   "/install/",
                                   MenuItem.LOGIN_MENU,
                                   SAWPermission.get_or_create("can_install"))]

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^install/",)

def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_install", WEBMASTER),
    )