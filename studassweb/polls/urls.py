from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'polls.views.home', name='polls_home'),
)
