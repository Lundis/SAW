from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST

def get_menu_items():
    return [MenuItem.get_or_create("contact",
                                   "Contact",
                                   "/contact/",
                                   MenuItem.MAIN_MENU,
                                   SAWPermission.get_or_create("can_view_contact_form"))]

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^contact/",)




def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_contact_form", GUEST, "Can view the contact form"),
        ("can_use_contact_form", GUEST, "Can use the contact form"),
    )