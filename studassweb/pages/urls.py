# coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='pages_view_categories'),

    url(r'^new_category$', views.edit_category, name='pages_new_category'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.view_category, name='pages_view_category'),
    url(r'^edit_category/(?P<category_id>\d+)$', views.edit_category, name='pages_edit_category'),
    url(r'^delete_category/(?P<category_id>\d+)$', views.delete_category, name='pages_delete_category'),

    url(r'^page/(?P<slug>[\w-]+)$', views.view_page, name='pages_view_page'),
    url(r'^page/(?P<slug>[\w-]+)/revision/(?P<revision_id>\d+)$', views.view_page, name='pages_view_page'),
    url(r'^new_page/(?P<category_id>\d+)$', views.edit_page, name='pages_new_page'),
    url(r'^new_page$', views.edit_page, name='pages_new_page'),
    url(r'^edit_page/(?P<page_id>\d+)$', views.edit_page, name='pages_edit_page'),
    url(r'^edit_page/(?P<page_id>\d+)/(?P<revision_id>\d+)$', views.edit_page, name='pages_edit_page'),
    url(r'^revert_page/(?P<revision_id>\d+)$', views.revert_page, name='pages_revert_page'),
    url(r'^delete_page/(?P<page_id>\d+)', views.delete_page, name='pages_delete_page')
]
