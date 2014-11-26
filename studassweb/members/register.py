from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import BOARD_MEMBER


def get_menu_items():
    return (None,
            [MenuItem.get_or_create(__package__,
                                    "Member Registry",
                                    reverse_string="members_home",
                                    permission=SAWPermission.get_or_create("can_view_member_registry"))],
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^members/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_member_registry", BOARD_MEMBER, "Can view the member registry"),
        ("can_edit_member_registry", BOARD_MEMBER, "Can edit information in the member registry"),
    )