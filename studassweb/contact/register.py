from django.core.urlresolvers import reverse_lazy

from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, BOARD_MEMBER
from settings.sections import Page, SECTION_OTHER



CAN_VIEW_CONTACT_INFO = "can_view_contact_info"
CAN_USE_CONTACT_FORM = "can_use_contact_form"
CAN_VIEW_MESSAGES = "can_view_messages"
CAN_EDIT_CONTACT_SETTINGS = "can_edit_contact_settings"


def get_menu_items():
    """
    :return: a tuple ([main menu items], [settings menu items], [others])
    """
    item, created = MenuItem.get_or_create(identifier="contact_home",
                                           app_name=__package__,
                                           display_name="Contact",
                                           reverse_string="contact_home",
                                           permission=SAWPermission.get(CAN_VIEW_CONTACT_INFO))
    return [item], None, None


def get_urls():
    """
    :returns: A tuple of regexes describing what URLs the top-level URL dispatcher should associate with this module
    """
    return r"^contact/",


def get_permissions():
    """
    :return: a list of tuples containing the permissions of this module and their default group
    """
    return (
        (CAN_VIEW_CONTACT_INFO, GUEST, "Can view the contact page"),
        (CAN_USE_CONTACT_FORM, GUEST, "Can send messages using the contact forms"),
        (CAN_VIEW_MESSAGES, BOARD_MEMBER, "Can view all sent messages"),
        (CAN_EDIT_CONTACT_SETTINGS, BOARD_MEMBER, "Can edit settings for contact module"),
    )


