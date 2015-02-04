from django.conf.urls import patterns, url
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from settings.sections import SECTION_OTHER, Section
from users.decorators import has_permission
from .forms import ContactSettingsForm
from .models import ContactInfo
from .register import CAN_EDIT_CONTACT_SETTINGS

urlpatterns = patterns(
    '',
    url(r'^%s/contacts/$' % SECTION_OTHER,
        'contact.settings_pages.list_contacts',
        name='contact_settings_list_contacts'),
    url(r'^%s/contacts/edit/(?P<contact_id>\d+)$' % SECTION_OTHER,
        'contact.settings_pages.edit_contact',
        name='contact_settings_edit_contact'),
    url(r'^%s/contacts/new$' % SECTION_OTHER,
        'contact.settings_pages.edit_contact',
        name='contact_settings_new_contact'),
)


@has_permission(CAN_EDIT_CONTACT_SETTINGS)
def list_contacts(request):
    """
    This view lists all the contact entities and lets the user pick one for editing
    :param request:
    :return:
    """
    section = Section.get_section(SECTION_OTHER)
    contacts = ContactInfo.objects.all()

    context = {'section': section,
               'contacts': contacts}
    return render(request, "contact/settings/list_contacts.html", context)


@has_permission(CAN_EDIT_CONTACT_SETTINGS)
def edit_contact(request, contact_id):
    section = Section.get_section(SECTION_OTHER)
    try:
        contact = ContactInfo.objects.get(id=contact_id)
    except ContactInfo.DoesNotExist:
        contact = None

    form = ContactSettingsForm(request.POST or None, instance=contact)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("contact_settings_list_contacts"))
    context = {'section': section,
               'form': form,
               'contact': contact}
    return render(request, "contact/settings/edit_contact.html", context)