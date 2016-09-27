# coding=utf-8
from django.conf.urls import url

from . import views
from . import ajax

urlpatterns = [
    url(r'^$', views.home, name='contact_home'),
    url(r'^$', views.home, name='contact_show_contact_info'),
    url(r'^write_message/(?P<contact_id>\d+)$',
        views.write_message,
        name='contact_write_message'),
    url(r'^send_confirmation$',
        views.send_confirmation,
        name='contact_send_confirmation'),
    url(r'^read_messages/(?P<contact_id>\d+)$',
        views.read_messages,
        name='contact_view_messages'),
    url(r'^delete_message/(?P<message_id>\d+)$',
        views.delete_message,
        name='contact_delete_message'),

    url(r'^edit_contact/(?P<contact_id>\d+)$',
        views.edit_contact,
        name='contact_edit'),
    url(r'^new_contact$',
        views.edit_contact,
        name='contact_create'),
    url(r'^delete_contact/(?P<contact_id>\d+)$',
        views.delete_contact,
        name='contact_delete'),
    url(r'^mark_message_as_handled$',
        ajax.mark_message_as_handled,
        name='contact_mark_message_as_handled')
]
