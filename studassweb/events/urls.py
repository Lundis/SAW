from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'events.views.home', name='events_home'),
    url(r'^get/(?P<event_id>\d+)/$', 'events.views.event_detail', name='events_view_event'),
    url(r'^add/$', 'events.views.add_event', name='events_add_event'),
    url(r'^edit/(?P<event_id>\d+)/$', 'events.views.edit_event', name='events_edit_event'),
    url(r'^delete/(?P<event_id>\d+)/$', 'events.views.delete_event', name='events_delete_event'),
)
