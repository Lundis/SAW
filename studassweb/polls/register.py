from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(__package__,
                                           "Polls",
                                           reverse_string="polls_home",
                                           permission=SAWPermission.get_or_create("can_view_polls"))
    return ([item],
            None,
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^polls/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_create_polls", BOARD_MEMBER, "Can create polls"),
        ("can_view_polls", GUEST, "Can view most polls"),
        ("can_view_member_polls", MEMBER, "Can view polls for members"),
        ("can_view_board_polls", BOARD_MEMBER, "Can view polls for board members"),
        ("can_vote_public_polls", GUEST, "Can vote in public polls"),
        ("can_vote_member_polls", MEMBER, "Can vote in member polls"),
        ("can_vote_board_polls", BOARD_MEMBER, "Can vote in polls for board members"),
    )