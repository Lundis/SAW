from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, BOARD_MEMBER

CAN_VIEW_FRONTPAGE = "can_view_frontpage"
CAN_EDIT_FRONTPAGE = "can_edit_frontpage"


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(identifier="frontpage_home",
                                           app_name=__package__,
                                           display_name="Home",
                                           reverse_string="frontpage_home",
                                           permission=SAWPermission.get_or_create(CAN_VIEW_FRONTPAGE))
    return ([item],
            None,
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^frontpage/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (CAN_VIEW_FRONTPAGE, GUEST, "Can view the frontpage"),
        (CAN_EDIT_FRONTPAGE, BOARD_MEMBER, "Can edit what’s visible on the front page"),
    )