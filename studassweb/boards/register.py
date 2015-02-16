from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, BOARD_MEMBER

CAN_VIEW_BOARDS = "can_view_boards"
CAN_EDIT_BOARDS = "can_edit_boards"
CAN_EDIT_ROLES = "can_edit_roles"
CAN_EDIT_BOARDTYPES = "can_edit_boardtypes"


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(identifier="boards_home",
                                           app_name=__package__,
                                           display_name="Board",
                                           reverse_string="boards_main",
                                           permission=SAWPermission.get_or_create(CAN_VIEW_BOARDS))
    return ([item],
            None,
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^boards/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (CAN_VIEW_BOARDS, GUEST, "Access to the page that shows the boards"),
        (CAN_EDIT_BOARDS, BOARD_MEMBER, "Can add/edit the board/committees for each year"),
        (CAN_EDIT_ROLES, BOARD_MEMBER, "Can add/edit the roles in a board"),
        (CAN_EDIT_BOARDTYPES, BOARD_MEMBER, "Can add/edit the different board types"),
    )
