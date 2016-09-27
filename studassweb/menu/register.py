# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from users.groups import WEBMASTER
from settings.sections import Page, SECTION_MENU, SECTION_APPEARANCE

EDIT_MENUS = "can_edit_menu"


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (EDIT_MENUS, WEBMASTER, "Can change the menu layout"),
    )


def register_settings_pages():
    item = Page("Menu Editor",
                "Add, remove and change the order of any menu on the site",
                SECTION_MENU,
                reverse_lazy('menu_settings_select_menu'),
                EDIT_MENUS)
    menu_layout = Page("Main Menu Appearance",
                       "Change the appearance of the main menu",
                       SECTION_APPEARANCE,
                       reverse_lazy("menu_settings_edit_menu_layout"),
                       EDIT_MENUS)
    return item, menu_layout


