from menu.models import MenuItem, Menu
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER
from .models import InfoPage
from .frontpage import InfoFrontPageItem


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(__package__,
                                           "Info",
                                           reverse_string="info_view_categories",
                                           permission=SAWPermission.get_or_create(VIEW_PUBLIC))
    if not item.submenu:
        item.submenu, created = Menu.objects.get_or_create(menu_name="info_top_menu")
        item.save()

    return [item], None, None


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^info/",


VIEW_PUBLIC = "can_view_public_info_pages"
VIEW_MEMBER = "can_view_member_info_pages"
VIEW_BOARD = "can_view_board_member_info_pages"
EDIT = "can_edit_info_pages"


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (VIEW_PUBLIC, GUEST, "Access to public of the information pages"),
        (VIEW_MEMBER, MEMBER, "Access to members-only information pages"),
        (VIEW_BOARD, BOARD_MEMBER, "Access to board-only information pages"),
        (EDIT, BOARD_MEMBER, "Can create and edit info pages"),
    )


def get_front_page_items():
    pages = InfoPage.objects.filter(for_front_page=True)
    items = ()
    for page in pages:
        items += InfoFrontPageItem(page),
    return items