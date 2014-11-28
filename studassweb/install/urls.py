from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'install.views.welcome', name='install_welcome'),
    url(r'^welcome$', 'install.views.welcome', name='install_welcome'),
    url(r'^association$', 'install.views.association', name='install_association'),
    url(r'^modules$', 'install.views.modules', name='install_modules'),
    url(r'^menu$', 'install.views.menu', name='install_menu'),
    url(r'^finished$', 'install.views.finished', name='install_finished'),
)
