from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='install_welcome'),
    url(r'^welcome$', views.welcome, name='install_welcome'),
    url(r'^association$', views.association, name='install_association'),
    url(r'^modules$', views.modules, name='install_modules'),
    url(r'^menu$', views.menu, name='install_menu'),
    url(r'^finished$', views.finished, name='install_finished'),
]
