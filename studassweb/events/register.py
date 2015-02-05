from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, BOARD_MEMBER

CAN_VIEW_EVENTS = "can_view_events"
CAN_SIGNUP_FOR_EVENTS = "can_signup_for_events"
CAN_CREATE_EVENTS = "can_create_events"
CAN_VIEW_SIGNUP_INFO = "can_view_signup_info"

def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(__package__,
                                           "Events",
                                           reverse_string="events_home",
                                           permission=SAWPermission.get_or_create(CAN_VIEW_EVENTS))
    return ([item],
            None,
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^events/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (CAN_VIEW_EVENTS, GUEST, "Can view events"),
        (CAN_SIGNUP_FOR_EVENTS, GUEST, "Can sign up for events"),
        (CAN_CREATE_EVENTS, BOARD_MEMBER, "Can create events"),
        (CAN_VIEW_SIGNUP_INFO, BOARD_MEMBER, "Can view normally hidden info about signed up people"),
    )