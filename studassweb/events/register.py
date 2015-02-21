from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER

CAN_CREATE_EVENTS = "can_create_events"
CAN_VIEW_SIGNUP_INFO = "can_view_signup_info"

CAN_VIEW_AND_JOIN_PUBLIC_EVENTS = "can_view_and_join_public_events"
CAN_VIEW_AND_JOIN_MEMBER_EVENTS = "can_view_and_join_board_member_events"
CAN_VIEW_AND_JOIN_BOARD_MEMBER_EVENTS = "can_view_and_join_board:member_events"


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(identifier="events_home",
                                           app_name=__package__,
                                           display_name="Events",
                                           reverse_string="events_home",
                                           permission=SAWPermission.get(CAN_VIEW_AND_JOIN_PUBLIC_EVENTS))
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
        (CAN_VIEW_AND_JOIN_PUBLIC_EVENTS, GUEST, "Can view and join public events"),
        (CAN_VIEW_AND_JOIN_MEMBER_EVENTS, MEMBER, "Can view and join member events"),
        (CAN_VIEW_AND_JOIN_BOARD_MEMBER_EVENTS, BOARD_MEMBER, "Can view and join board member events"),
        (CAN_CREATE_EVENTS, BOARD_MEMBER, "Can create events"),
        (CAN_VIEW_SIGNUP_INFO, BOARD_MEMBER, "Can view normally hidden info about signed up people"),
    )
