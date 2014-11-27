from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import LOGGED_ON

VIEW_SETTINGS = "can_view_settings"


def get_permissions():
    """
    :return: a tuple of tuples containing the permissions of this module and their default group
    """
    return (
        (VIEW_SETTINGS, LOGGED_ON, "Access to the settings page"),
    )


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(__package__,
                                           "Settings",
                                           reverse_string="settings_main",
                                           permission=SAWPermission.get_or_create(VIEW_SETTINGS))
    return (None,
            [item],
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^settings/",