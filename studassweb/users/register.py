from django.core.urlresolvers import reverse_lazy
from users.groups import MEMBER, LOGGED_ON, WEBMASTER
from menu.models import MenuItem
from users.models import SAWPermission
from settings.sections import Page, SECTION_PERSONAL_SETTINGS, SECTION_USERS


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^users/",


VIEW_PROFILES = "can_view_profiles"
EDIT_PROFILE = "can_edit_profile"
EDIT_PERMISSIONS = "can_edit_permissions"
EDIT_LOGIN_SETTINGS = "can_edit_login_settings"


def get_permissions():
    """
    :return: a tuple of tuples containing the permissions of this module and their default group
    """
    return (
        (VIEW_PROFILES, MEMBER, "Can view the profile pages of other users"),
        (EDIT_PROFILE, LOGGED_ON, "Access to the settings page for editing personal user settings"),
        (EDIT_PERMISSIONS, WEBMASTER, "Access to the settings page for permissions"),
        (EDIT_LOGIN_SETTINGS, WEBMASTER,
         "Access to the settings page for configuring how users can log in (LDAP, FB, G+ etc)"),
    )


def register_settings_pages():
    profile = Page("Personal Settings",
                   SECTION_PERSONAL_SETTINGS,
                   reverse_lazy("users_settings_edit_user"),
                   EDIT_PROFILE)
    permissions = Page("Groups and Permissions",
                       SECTION_USERS,
                       reverse_lazy("users_settings_edit_permissions"),
                       EDIT_PERMISSIONS)
    login = Page("User settings",
                 SECTION_USERS,
                 reverse_lazy("users_settings_edit_login"),
                 EDIT_LOGIN_SETTINGS)
    return profile, permissions, login
