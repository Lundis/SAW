from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER

def get_menu_items():
    return [MenuItem.get_or_create("info",
                                   "Info",
                                   "/info/",
                                   MenuItem.MAIN_MENU,
                                   SAWPermission.get_or_create("can_view_public_info_pages"))]

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^info/",)



def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_public_info_pages", GUEST, "Access to most of the information pages"),
        ("can_view_member_info_pages", MEMBER, "Access to all information pages"),
        ("can_edit_info_pages", BOARD_MEMBER, "Can create and edit info pages"),
    )