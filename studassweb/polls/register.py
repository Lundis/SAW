from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER

CAN_CREATE_POLLS = "can_create_polls"
CAN_VIEW_PUBLIC_POLLS = "can_view_public_polls"
CAN_VIEW_MEMBER_POLLS = "can_view_member_polls"
CAN_VIEW_BOARD_POLLS = "can_view_board_polls"
CAN_VOTE_PUBLIC_POLLS = "can_vote_public_polls"
CAN_VOTE_MEMBER_POLLS = "can_vote_member_polls"
CAN_VOTE_BOARD_POLLS = "can_vote_board_polls"
CAN_DELETE_ALL_POLLS = "can_delete_all_polls"


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(identifier="polls_home",
                                           app_name=__package__,
                                           display_name="Polls",
                                           reverse_string="polls_home",
                                           permission=SAWPermission.get_or_create(CAN_VIEW_PUBLIC_POLLS))
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
        (CAN_CREATE_POLLS, MEMBER, "Can create polls"),
        (CAN_VIEW_PUBLIC_POLLS, GUEST, "Can view most polls"),
        (CAN_VIEW_MEMBER_POLLS, MEMBER, "Can view polls for members"),
        (CAN_VIEW_BOARD_POLLS, BOARD_MEMBER, "Can view polls for board members"),
        (CAN_VOTE_PUBLIC_POLLS, GUEST, "Can vote in public polls"),
        (CAN_VOTE_MEMBER_POLLS, MEMBER, "Can vote in member polls"),
        (CAN_VOTE_BOARD_POLLS, BOARD_MEMBER, "Can vote in polls for board members"),
        (CAN_DELETE_ALL_POLLS, BOARD_MEMBER, "Can delete other members polls"),
    )