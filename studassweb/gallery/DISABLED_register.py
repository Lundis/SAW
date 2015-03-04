from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER

CAN_VIEW_PUBLIC_ALBUMS = "can_view_public_albums"
CAN_VIEW_MEMBER_ALBUMS = "can_view_member_albums"
CAN_CREATE_ALBUMS = "can_create_albums"
CAN_EDIT_MEMBER_ALBUMS = "can_edit_member_albums"
CAN_EDIT_ALL_ALBUMS = "can_edit_all_albums"

DESCRIPTION = "A simple image gallery. Create albums, upload images to them and select who should be able to view them"


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(identifier="gallery_home",
                                           app_name=__package__,
                                           display_name="Gallery",
                                           reverse_string="gallery_main",
                                           permission=SAWPermission.get(CAN_VIEW_PUBLIC_ALBUMS))
    return ([item],
            None,
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^gallery/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (CAN_VIEW_PUBLIC_ALBUMS, GUEST, "Can view most albums"),
        (CAN_VIEW_MEMBER_ALBUMS, MEMBER, "Can view all albums"),
        (CAN_CREATE_ALBUMS, BOARD_MEMBER, "Can create albums"),
        (CAN_EDIT_MEMBER_ALBUMS, MEMBER, "Can upload images to albums that are for members"),
        (CAN_EDIT_ALL_ALBUMS, BOARD_MEMBER, "Can edit descriptions, upload and remove images to/from all albums"),
    )