# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from users.groups import MEMBER, LOGGED_ON, WEBMASTER
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
        (EDIT_PERMISSIONS, WEBMASTER, "Access to settings for groups and permissions"),
        (EDIT_LOGIN_SETTINGS, WEBMASTER,
         "Access to the settings page for configuring how users can log in (LDAP, FB, G+ etc)"),
    )


def register_settings_pages():
    profile = Page("Personal Settings",
                   "Edit your contact details and other personal information",
                   SECTION_PERSONAL_SETTINGS,
                   reverse_lazy("users_settings_edit_user"),
                   EDIT_PROFILE)
    permissions = Page("Permissions",
                       "Change which standard groups have which permissions",
                       SECTION_USERS,
                       reverse_lazy("users_settings_edit_permissions"),
                       EDIT_PERMISSIONS)
    """
    groups = Page("Custom groups",
                  "Make your own groups with specialized permissions",
                  SECTION_USERS,
                  reverse_lazy("users_settings_edit_groups"),
                  EDIT_PERMISSIONS)
    """
    login = Page("Login settings",
                 "Change how users can log in",
                 SECTION_USERS,
                 reverse_lazy("users_settings_edit_login"),
                 EDIT_LOGIN_SETTINGS)
    return profile, permissions, login,  # groups

