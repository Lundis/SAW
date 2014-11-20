from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER

def get_menu_items():
    return [MenuItem.get_or_create("gallery",
                                   "Gallery",
                                   "/gallery/",
                                   MenuItem.MAIN_MENU,
                                   SAWPermission.get_or_create("can_view_public_albums"))]

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^gallery/",)



def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_public_albums", GUEST, "Can view most albums"),
        ("can_view_member_albums", MEMBER, "Can view all albums"),
        ("can_create_albums", BOARD_MEMBER, "Can create albums"),
        ("can_edit_member_albums", MEMBER, "Can upload images to albums that are for members"),
        ("can_edit_all_albums", BOARD_MEMBER, "Can edit descriptions, upload and remove images to/from all albums"),
    )