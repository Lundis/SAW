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
)
if settings.MEDIA_DJANGO:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if not InstallProgress.is_finished():
    # Disable all modules to make sure that the pages aren't accessed before installed
    for module in settings.OPTIONAL_APPS:
        DisabledModule.disable(module)

# Add the urlpatterns of all modules
for mod, url_func in get_modules_with("register", "get_urls"):
    for url_pattern in url_func():
        urlpatterns += (url(url_pattern, include(mod + ".urls")),)
