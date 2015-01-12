from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, MEMBER, BOARD_MEMBER

VIEW_PUBLIC = "can_view_public_news"
VIEW_MEMBER = "can_view_member_news"
EDIT_PUBLIC = "can_create_news"


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(__package__,
                                           "News",
                                           reverse_string="news_home",
                                           permission=SAWPermission.get_or_create(VIEW_PUBLIC))
    return ([item],
            None,
            None)


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^news/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (VIEW_PUBLIC, GUEST, "Access to public news articles"),
        (VIEW_MEMBER, MEMBER, "Access to all news articles"),
        (EDIT_PUBLIC, BOARD_MEMBER, "Can create news articles"),
    )