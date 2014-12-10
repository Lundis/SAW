from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'events.views.home', name='events_home'),
    url(r'^past/$', 'events.views.archive', name='archive'),
    url(r'^get/(?P<entry_id>\d+)/$', 'events.views.event_detail', name='events_detail'),
    url(r'^new/$', 'events.views.add_event', name='add_event'),
    url(r'^like/(?P<entry_id>\d+)/$', 'events.views.attend_status', name='attend_status'),
    url(r'^edit/(?P<entry_id>\d+)/$', 'events.views.edit_event', name='edit_events'),
    url(r'^comment/(?P<entry_id>\d+)/$', 'events.views.comment', name='comment'),
    url(r'^past-events/$', 'events.views.archive', name='archive'),

)
