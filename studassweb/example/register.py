def getMenuItems():
    """
    :return: a list of menu.models.MenuItem
    """
    pass

def getUrls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^example/",)