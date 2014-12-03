from django.conf.urls import patterns, url
from users.decorators import has_permission
from django.shortcuts import render
from .models import SiteConfiguration

from .register import EDIT_THEME

urlpatterns = patterns('',
    url(r'^edit_themes$',
        'base.settings_pages.edit_theme',
        name='base_settings_edit_theme'),
)

@has_permission(EDIT_THEME)
def edit_theme(request):
    SiteConfiguration.update_bootswatch()
    context = {}
    return render(request, 'base/settings/theme_editor.html', context)