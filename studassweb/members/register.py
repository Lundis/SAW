from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import BOARD_MEMBER

def get_menu_items():
    return [MenuItem.get_or_create("members",
                                   "Member Registry",
                                   "/members/",
                                   MenuItem.LOGIN_MENU,
                                   SAWPermission.get_or_create("can_view_member_registry"))]


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^members/",)

def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_member_registry", BOARD_MEMBER),
        ("can_edit_member_registry", BOARD_MEMBER),
    )