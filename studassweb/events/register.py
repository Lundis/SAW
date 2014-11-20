from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, BOARD_MEMBER

def get_menu_items():
    return [MenuItem.get_or_create("events",
                                   "Events",
                                   "/events/",
                                   MenuItem.MAIN_MENU,
                                   SAWPermission.get_or_create("can_view_events"))]

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^events/",)



def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_events", GUEST, "Can view events"),
        ("can_signup_for_events", GUEST, "Can sign up for events"),
        ("can_create_events", BOARD_MEMBER, "Can create events"),
    )