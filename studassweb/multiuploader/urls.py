from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^multiuploader/$', views.multiuploader, name='multiuploader'),
        url(r'^multiuploader_noajax/$', views.multiuploader, kwargs={"noajax": True},
            name='multiploader_noajax'),
    ]
