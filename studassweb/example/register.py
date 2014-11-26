from menu.models import MenuItem


def get_menu_items():
    return (None,
            None,
            [MenuItem.get_or_create(__package__,
                                    "Example",
                                    reverse_string="example_choose")])


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^example/",