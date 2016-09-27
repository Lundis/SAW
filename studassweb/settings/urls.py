from django.conf.urls import url, include
from base.utils import get_modules_with

from . import views

urlpatterns = [
    url(r'^$', views.view_sections, name='settings_main'),
    url(r'^(?P<section_id>[a-zA-Z_]+)$', views.view_section, name='settings_view_section'),
]

# link all modules that have registered settings pages
for module, get_pages in get_modules_with("register", "register_settings_pages"):
    if len(get_pages()) > 0:
        settings_url = module + ".settings_pages"
        urlpatterns.append(
            url(r'', include(settings_url))
        )
