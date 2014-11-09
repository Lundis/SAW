from menu.models import MenuItem
from users.models import SAWPermission

def get_menu_items():
    return [MenuItem.get_or_create("polls",
                                   "Polls",
                                   "/polls/",
                                   MenuItem.NONE,
                                   SAWPermission.get_or_create("can_view_polls"))]

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^polls/",)