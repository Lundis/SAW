from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'login.views.login', name='login'),
)