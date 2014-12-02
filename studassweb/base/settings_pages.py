from django.conf.urls import patterns, url
from users.decorators import has_permission
from django.shortcuts import render
from urllib.request import urlopen
import json

from .register import EDIT_THEME

urlpatterns = patterns('',
    url(r'^edit_themes$',
        'base.settings_pages.edit_theme',
        name='base_settings_edit_theme'),
)

@has_permission(EDIT_THEME)
def edit_theme(request):
    # http://bootswatch.com/help/#api
    data = urlopen("http://api.bootswatch.com/3/").read().decode()
    data_dict = json.loads(data)
    context = {}
    return render(request, 'base/settings/theme_editor.html', context)