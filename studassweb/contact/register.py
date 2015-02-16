from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from menu.models import MenuItem
from users.models import SAWPermission
from users.groups import GUEST, BOARD_MEMBER
from settings.sections import Page, SECTION_OTHER
from base.models import SiteConfiguration
import contact.models as cmodels

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
                                           permission=SAWPermission.get_or_create(CAN_VIEW_CONTACT_INFO))
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


def setup():
    """
    Creates a default contact group for the association
    :return:
    """
    # First check if the module has been set up before
    if not cmodels.ContactSettings.is_setup():
        contact = cmodels.ContactInfo(name=_("The Board"),
                                      save_to_db=True,
                                      send_email=True,
                                      email=SiteConfiguration.instance().association_contact_email,
                                      ordering_index=1
                                      )
        contact.save()

        contact = cmodels.ContactInfo(name=_("The developers"),
                                      info_text=_("Give feedback and report bugs to the developers!"),
                                      save_to_db=False,
                                      send_email=True,
                                      email="SAW.errors@gmail.com",
                                      ordering_index=99
                                      )
        contact.save()
        settings = cmodels.ContactSettings.objects.get()
        settings._is_setup = True
        settings.save()
