from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(__package__,
                                           "Contact",
                                           reverse_string="contact_home",
                                           permission=SAWPermission.get_or_create("can_view_contact_form"))
    return [item], None, None


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^contact/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_contact_form", GUEST, "Can view the contact form"),
        ("can_use_contact_form", GUEST, "Can use the contact form"),
    )