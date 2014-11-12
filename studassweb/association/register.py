from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, BOARD_MEMBER

def get_menu_items():
    return [MenuItem.get_or_create("association",
                                   "Association",
                                   "/association/",
                                   MenuItem.MAIN_MENU,
                                   SAWPermission.get_or_create("can_view_association"))]


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^association/",)

def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_association", GUEST),
        ("can_edit_association", BOARD_MEMBER),
    )
