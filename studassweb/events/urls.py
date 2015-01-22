from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'events.views.home', name='events_home'),
    url(r'^past/$', 'events.views.archive', name='events_archive'),
    url(r'^get/(?P<event_id>\d+)/$', 'events.views.event_detail', name='events_view_event'),
    url(r'^new/$', 'events.views.add_event', name='events_add_event'),
    url(r'^attend/(?P<event_id>\d+)/$', 'events.views.attend_status', name='events_attend'),
    url(r'^edit/(?P<event_id>\d+)/$', 'events.views.edit_event', name='events_edit_event'),
    url(r'^delete/(?P<event_id>\d+)/$', 'events.views.delete_event', name='events_delete_event'),
    #url(r'^comment/(?P<entry_id>\d+)/$', 'events.views.comment', name='events_comment'),
)
