from django.conf.urls import patterns, url
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from users.decorators import has_permission
from .models import SiteConfiguration, BootswatchTheme, THEME_DEFAULT_CSS, THEME_DEFAULT_CSS_MOD
from .register import EDIT_THEME
from .forms import BootswatchThemeSelectForm
from settings.sections import SECTION_APPEARANCE, Section
import logging

logger = logging.getLogger(__name__)

urlpatterns = patterns('',
    url(r'^%s/edit_themes$' % SECTION_APPEARANCE,
        'base.settings_pages.edit_theme',
        name='base_settings_edit_theme'),
    url(r'^%s/set_bootswatch_theme$' % SECTION_APPEARANCE,
        'base.settings_pages.set_bootswatch_theme',
        name='base_settings_set_bootswatch_theme'),
    url(r'^%s/set_theme$' % SECTION_APPEARANCE,
        'base.settings_pages.set_default_theme',
        name='base_settings_set_default_theme'),
)


@has_permission(EDIT_THEME)
def edit_theme(request):
    SiteConfiguration.update_bootswatch()
    section = Section.get_section(SECTION_APPEARANCE)
    context = {'themes': BootswatchTheme.objects.all(),
               'section': section}
    return render(request, 'base/settings/theme_editor.html', context)


@has_permission(EDIT_THEME)
def set_bootswatch_theme(request):
    if not request.POST:
        raise Http404
    else:
        form = BootswatchThemeSelectForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            logger.warn("Setting Bootswatch theme failed!")
        return HttpResponseRedirect(reverse('base_settings_edit_theme'))

@has_permission(EDIT_THEME)
def set_default_theme(request):
    if not request.POST:
        raise Http404
    else:
        settings = SiteConfiguration.instance()
        settings.bootstrap_theme_url = THEME_DEFAULT_CSS
        settings.bootstrap_theme_mod_url = THEME_DEFAULT_CSS_MOD
        settings.save()
        return HttpResponseRedirect(reverse('base_settings_edit_theme'))
