def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^users/",)

from users.groups import MEMBER, LOGGED_ON, WEBMASTER

def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        ("can_view_profiles", MEMBER),
        ("can_edit_profile", LOGGED_ON),
        ("can_edit_permissions", WEBMASTER),
        ("can_edit_login_settings", WEBMASTER),
    )