from django.conf.urls import patterns, url
from .views import AddEventItemView, EditEventItemView, DeleteEventItemView, ListEventItemsView, DeleteEventSignupByCodeView

slug_pattern = '(?P<slug>[-\w\d]+)'

urlpatterns = patterns('',

    url(r'^$', 'events.views.home', name='events_home'),

    # url(r'^event/(?P<event_id>\d+)/$',
    #    'events.views.event_detail',
    #    name='events_view_event'),

    url(r'^event/%s/$' % slug_pattern,
        'events.views.event_detail',
        name='events_view_event'),
    url(r'^event/(?P<event_id>\d+)/edit_signup_by_id/(?P<signup_id>\d+)$',
        'events.views.event_detail',
        name='events_view_event_edit_signup_by_id'),
    url(r'^event/(?P<event_id>\d+)/edit_signup_by_code/(?P<auth_code>[a-z0-9]{32})$',
        'events.views.event_detail',
        name='events_view_event_edit_signup_by_code'),

    url(r'^add/$', 'events.views.add_event', name='events_add_event'),
    url(r'^edit/(?P<event_id>\d+)/$', 'events.views.edit_event', name='events_edit_event'),
    url(r'^delete/(?P<event_id>\d+)/$', 'events.views.delete_event', name='events_delete_event'),
    url(r'^delete_signup/(?P<event_signup_id>\d+)/$',
        'events.views.delete_event_signup',
        name='events_delete_event_signup'),
    url(r'^delete_signup/(?P<auth_code>[a-z0-9]{32})$',
        DeleteEventSignupByCodeView.as_view(),
        name='events_delete_event_signup_by_code'),
    url(r'^add_event_item/$', AddEventItemView.as_view(), name='events_add_eventitem'),
    url(r'^edit_event_item/(?P<pk>\d+)/$', EditEventItemView.as_view(), name='events_edit_eventitem'),
    url(r'^delete_event_item/(?P<pk>\d+)/$', DeleteEventItemView.as_view(), name='events_delete_eventitem'),
    url(r'^list_event_items/$', ListEventItemsView.as_view(), name='events_list_eventitems'),
)
