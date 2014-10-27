from django.conf.urls import patterns, include, url
from django.contrib import admin
from base.utils import get_modules_with, get_function_from_module
from base.models import DisabledModule

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studassweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
#    url(r'^$', include('frontpage.urls')),
#    url(r'^info/', include('info.urls')),
#    url(r'^settings/', include('settings.urls')),
#    url(r'^install/', include('install.urls')),
#    url(r'^login/', include('login.urls')),
)

for mod in get_modules_with("register", "get_urls"):
    if DisabledModule.is_enabled(mod):
        get_urls = get_function_from_module(mod, "register", "get_urls")
        for url_pattern in get_urls():
            urlpatterns += (url(url_pattern, include(mod + ".urls")),)