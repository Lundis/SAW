from django.conf.urls import patterns, url
from settings.sections import Page, SECTION_OTHER, Section
from .register import CAN_EDIT_CONTACT_SETTINGS
from users.decorators import has_permission
from django.shortcuts import render
from .forms import SettingsForm
from .models import Settings

urlpatterns = patterns(
    '',
    url(r'^%s/contact_module/$' % SECTION_OTHER,
    'contact.settings_pages.edit_settings',
    name='contact_settings_edit_settings'),
)

@has_permission(CAN_EDIT_CONTACT_SETTINGS)
def edit_settings(request):
    section = Section.get_section(SECTION_OTHER)
    settings = Settings.get_solo()

    form = SettingsForm(request.POST or None, instance=settings)
    if form.is_valid():
        form.save()
    context = {'section': section, 'form': form}
    return render(request, "contact/settings.html", context)