from users.groups import WEBMASTER
from menu.models import MenuItem
from users.models import SAWPermission


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_edit_menu", WEBMASTER, "Can change the menu layout"),
    )

def get_settings_items():
    return [MenuItem.get_or_create(__package__,
                                   "Menu items",
                                   "/settings/menu",
                                   permission=SAWPermission.get_or_create("can_edit_menu"))
    ]