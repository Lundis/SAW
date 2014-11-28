from django.conf.urls import patterns, include, url
from django.contrib import admin
from base.utils import get_modules_with
from base.models import DisabledModule
from install.models import InstallProgress
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
)\
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #development!

if not InstallProgress.is_finished():
    urlpatterns += (
        url(r'^install/', include("install.urls")),
        url(r'^$', "install.views.welcome"),
    )
    for pat in urlpatterns:
        print(pat)
else:
    for mod, url_func in get_modules_with("register", "get_urls"):
        if DisabledModule.is_enabled(mod):
            for url_pattern in url_func():
                urlpatterns += (url(url_pattern, include(mod + ".urls")),)
