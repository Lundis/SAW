from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER

def get_menu_items():
    return [MenuItem.get_or_create("polls",
                                   "Polls",
                                   "/polls/",
                                   MenuItem.NONE,
                                   SAWPermission.get_or_create("can_view_polls"))]

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^polls/",)


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_create_polls", BOARD_MEMBER),
        ("can_view_polls", GUEST),
        ("can_view_member_polls", MEMBER),
        ("can_view_board_polls", BOARD_MEMBER),
        ("can_vote_public_polls", GUEST),
        ("can_vote_member_polls", MEMBER),
        ("can_vote_board_polls", BOARD_MEMBER),
    )