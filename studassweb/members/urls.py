from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'members.views.view_members', name='members_home'),
)