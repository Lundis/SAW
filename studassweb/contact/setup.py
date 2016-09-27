# coding=utf-8
import contact.models as cmodels
from base.models import SiteConfiguration
from django.utils.translation import ugettext as _


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
