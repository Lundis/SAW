from menu.models import MenuItem
from users.models import SAWPermission

def get_menu_items():
    return [MenuItem.get_or_create("members",
                                   "Member Registry",
                                   "/members/",
                                   MenuItem.LOGIN_MENU,
                                   SAWPermission("can_view_member_registry"))]


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^members/",)