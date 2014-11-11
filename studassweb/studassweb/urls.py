from django.conf.urls import patterns, include, url
from django.contrib import admin
from base.utils import get_modules_with, get_function_from_module
from base.models import DisabledModule

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

for mod, url_func in get_modules_with("register", "get_urls"):
    if DisabledModule.is_enabled(mod):
        for url_pattern in url_func():
            urlpatterns += (url(url_pattern, include(mod + ".urls")),)


