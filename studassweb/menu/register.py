from users.groups import WEBMASTER
from menu.models import MenuItem
from users.models import SAWPermission

EDIT_MENUS = "can_edit_menu"


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (EDIT_MENUS, WEBMASTER, "Can change the menu layout"),
    )


def get_settings_items():
    item, created = MenuItem.get_or_create(__package__,
                                           'Menu items',
                                           reverse_string='menu_settings_select_menu',
                                           permission=SAWPermission.get_or_create(EDIT_MENUS))
    return [item]