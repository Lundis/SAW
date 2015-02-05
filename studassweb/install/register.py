from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import WEBMASTER


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(__package__,
                                           "Install",
                                           reverse_string="install_welcome",
                                           permission=SAWPermission.get_or_create(CAN_INSTALL))
    return (None,
            [item],
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^install/",


CAN_INSTALL = "can_install"


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (CAN_INSTALL, WEBMASTER, "Access to the installation wizard"),
    )