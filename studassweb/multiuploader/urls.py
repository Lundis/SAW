from django.conf.urls import patterns, url

urlpatterns =\
    patterns(
        '',
        url(r'^multiuploader/$', 'multiuploader.views.multiuploader', name='multiuploader'),
        url(r'^multiuploader_noajax/$', 'multiuploader.views.multiuploader', kwargs={"noajax": True},
            name='multiploader_noajax'),
    )
