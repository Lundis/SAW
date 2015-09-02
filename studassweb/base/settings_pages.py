from django.conf.urls import patterns, url
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from users.decorators import has_permission
from .models import SiteConfiguration, BootswatchTheme, THEME_DEFAULT_CSS, THEME_DEFAULT_CSS_MOD, \
    CSSOverrideContent, CSSOverrideFile
from .register import EDIT_THEME
from .forms import BootswatchThemeSelectForm, CSSOverrideFileForm, CSSOverrideContentForm
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

    url(r'^%s/css_overrides$' % SECTION_APPEARANCE,
        'base.settings_pages.view_css_overrides',
        name='base_settings_view_css_overrides'),

    url(r'^%s/css_overrides/new/from/(?P<copy_id>\d+)$' % SECTION_APPEARANCE,
        'base.settings_pages.edit_css_override',
        name='base_settings_new_css_override'),

    url(r'^%s/css_overrides/new$' % SECTION_APPEARANCE,
        'base.settings_pages.edit_css_override',
        name='base_settings_new_css_override'),

    url(r'^%s/css_overrides/(?P<file_id>\d+)$' % SECTION_APPEARANCE,
        'base.settings_pages.edit_css_override',
        name='base_settings_edit_css_file'),

    url(r'^%s/css_overrides/save/(?P<file_id>\d+)$' % SECTION_APPEARANCE,
        'base.settings_pages.edit_css_override',
        name='base_settings_save_css_override'),

    url(r'^%s/css_overrides/save$' % SECTION_APPEARANCE,
        'base.settings_pages.edit_css_override',
        name='base_settings_save_css_override'),

    url(r'^%s/css_overrides/set/(?P<override_id>\d+)$' % SECTION_APPEARANCE,
        'base.settings_pages.set_css_override',
        name='base_settings_set_css_override'),
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


@has_permission(EDIT_THEME)
def view_css_overrides(request):
    """
    View all created css override files.
    :param request:
    :return:
    """
    files = CSSOverrideFile.objects.all()
    section = Section.get_section(SECTION_APPEARANCE)
    current_override = SiteConfiguration.get_css_override()
    return render(request, "base/settings/view_css_overrides.html",
                  {'files': files,
                   'section': section,
                   'current_override': current_override})


@has_permission(EDIT_THEME)
def edit_css_override(request, file_id=None, copy_id=None):
    """
    Main view for css override editing. The file form is for renaming
    :param request:
    :param file_id:
    :param copy_id: id of file to read initial values from
    :return:
    """
    file = None
    content = None

    if file_id is not None:
        try:
            file = CSSOverrideFile.objects.get(id=file_id)
            content = file.get_latest_content()
        except CSSOverrideFile.DoesNotExist:
            raise Http404("Could not find specified file")

    if copy_id is not None:
        try:
            content = CSSOverrideContent.objects.get(id=copy_id)
        except CSSOverrideContent.DoesNotExist:
            raise Http404("Could not find specified content")

    file_form = CSSOverrideFileForm(request.POST or None,
                                    instance=file)
    initial = {}

    if content is not None:
        initial["css"] = content.css

    content_form = CSSOverrideContentForm(request.POST or None,
                                          initial=initial)

    if file_form.is_valid() and content_form.is_valid():
        file = file_form.save()
        override = content_form.save(user=request.user, file=file)
        SiteConfiguration.set_css_override(override)
        return HttpResponseRedirect(reverse("base_settings_view_css_overrides"))

    section = Section.get_section(SECTION_APPEARANCE)

    return render(request, "base/settings/edit_css_override.html",
                  {'file': file,
                   'file_form': file_form,
                   'content': content,
                   'content_form': content_form,
                   'section': section})


@has_permission(EDIT_THEME)
def set_css_override(request, override_id):
    """

    :param override_id:
    :return:
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if override_id is None:
        raise Http404("override_id was null!")

    try:
        override = CSSOverrideContent.objects.get(id=override_id)
    except CSSOverrideContent.DoesNotExist:
        raise Http404("override_id doesn't point to an existing CSSOverrideContent")

    SiteConfiguration.set_css_override(override)

    return HttpResponseRedirect(reverse('base_settings_view_css_overrides'))
