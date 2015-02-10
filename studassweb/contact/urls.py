from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'contact.views.home', name='contact_home'),
    url(r'^$', 'contact.views.home', name='contact_show_contact_info'),
    url(r'^write_message/(?P<contact_id>\d+)$', 'contact.views.write_message', name='contact_write_message'),
    url(r'^read_messages/(?P<contact_id>\d+)$', 'contact.views.read_messages', name='contact_view_messages'),
    url(r'^delete_message/(?P<message_id>\d+)$', 'contact.views.delete_message', name='contact_delete_message'),

    url(r'^edit_contact/(?P<contact_id>\d+)$',
        'contact.views.edit_contact',
        name='contact_edit'),
    url(r'^new_contact$',
        'contact.views.edit_contact',
        name='contact_create'),
    url(r'^delete_contact/(?P<contact_id>\d+)$',
        'contact.views.delete_contact',
        name='contact_delete'),
)
