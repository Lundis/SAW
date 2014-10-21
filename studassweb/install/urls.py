from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'install.views.welcome', name='welcome'),
    url(r'^welcome$', 'install.views.welcome', name='welcome'),
    url(r'^association$', 'install.views.association', name='association'),
    url(r'^modules$', 'install.views.modules', name='modules'),
    url(r'^menu$', 'install.views.menu', name='menu'),
    url(r'^finished$', 'install.views.finished', name='finished'),
)
