from users.groups import MEMBER, LOGGED_ON, WEBMASTER
from menu.models import MenuItem
from users.models import SAWPermission


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return (r"^users/",)


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


def get_settings_items():
    return [MenuItem.get_or_create("users",
                                   "User",
                                   "/settings/user",
                                   permission=SAWPermission.get_or_create("can_edit_profile")),
            MenuItem.get_or_create("users",
                                   "Permissions",
                                   "/settings/permissions",
                                   permission=SAWPermission.get_or_create("can_edit_permissions")),
            MenuItem.get_or_create("users",
                                   "Login",
                                   "/settings/login",
                                   permission=SAWPermission.get_or_create("can_edit_login_settings"))
    ]