def get_menu_items():
    """
    :return: a list of menu.models.MenuItem
    """
    pass

def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^example/",)