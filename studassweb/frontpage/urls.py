from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'frontpage.views.frontpage', name='frontpage_home'),
)