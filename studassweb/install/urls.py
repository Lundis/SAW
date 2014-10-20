from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'install.views.first_time_install', name='examplechoose'),
)
