from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'settings.views.main', name='settings_main'),
)
