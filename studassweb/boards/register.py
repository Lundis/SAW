from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, BOARD_MEMBER


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(__package__,
                                           "Board",
                                           reverse_string="boards_main",
                                           permission=SAWPermission.get_or_create("can_view_board"))
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
        ("can_view_boards", GUEST, "Access to the page that shows the boards"),
        ("can_edit_board", BOARD_MEMBER, "Can add/edit the board/committees for each year"),
        ("can_edit_roles", BOARD_MEMBER, "Can add/edit the roles in a board"),
        ("can_edit_boardtype", BOARD_MEMBER, "Can add/edit the different board types"),
    )
