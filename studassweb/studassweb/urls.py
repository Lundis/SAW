# coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from base.utils import get_modules_with
from django.conf import settings
from django.conf.urls.static import static
from django.db.utils import OperationalError

from frontpage import views

import logging

logger = logging.getLogger(__name__)

urlpatterns = [
    url(r'^$', views.frontpage, name='frontpage_home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.MEDIA_DJANGO:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add the urlpatterns of all modules
for mod, url_func in get_modules_with("register", "get_urls"):
    # recent django versions run this code before initing the DB, so we have to catch the failure of the settings module
    try:
        for url_pattern in url_func():
            urlpatterns.append(url(url_pattern, include(mod + ".urls")))
    except OperationalError:
        logger.warning("URL loading failed for module '" + mod + "' because the database hasn't been set up yet")
