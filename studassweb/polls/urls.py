# coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',                                      views.home,                 name='polls_home'),
    url(r'^poll/(?P<poll_id>\d+)$',                 views.view_poll,            name='polls_view_poll'),
    url(r'^add_poll/$',                             views.add_poll,             name='polls_add_poll'),
    url(r'^remove_poll/(?P<poll_id>\d+)$',          views.delete_poll,          name='polls_delete_poll'),
    url(r'^edit_poll/(?P<poll_id>\d+)$',            views.edit_poll,            name='polls_edit_poll'),
]
