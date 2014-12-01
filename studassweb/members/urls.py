from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'members.views.view_members', name='members_home'),
    url(r'^apply_membership$', 'members.views.apply_membership', name='members_apply_membership'),
)