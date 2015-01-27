from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'contact.views.home', name='contact_home'),
    url(r'^$', 'contact.views.home', name='contact_show_contact_info'),
    url(r'^write_message/$', 'contact.views.write_message', name='contact_write_message'),
    url(r'^read_messages/$', 'contact.views.read_messages', name='contact_read_messages'),
    url(r'^delete_message/(?P<message_id>\d+)$', 'contact.views.delete_message', name='contact_delete_message'),
)
