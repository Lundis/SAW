# coding=utf-8
from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import BOARD_MEMBER


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(identifier="members_home",
                                           app_name=__package__,
                                           display_name="Member Registry",
                                           reverse_string="members_home",
                                           permission=SAWPermission.get(CAN_VIEW))
    return (None,
            [item],
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^members/",


CAN_VIEW = "can_view_member_registry"
CAN_EDIT = "can_edit_member_registry"


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (CAN_VIEW, BOARD_MEMBER, "Can view the member registry"),
        (CAN_EDIT, BOARD_MEMBER, "Can edit information in the member registry"),
    )
