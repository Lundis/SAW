from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'info.views.main', name='view categories'),
    url(r'^new$', 'info.views.edit_category', name='view categories'),
    url(r'^(?P<category_id>\d+)/$', 'info.views.view_category', name='view category'),
    url(r'^(?P<category_id>\d+)/edit$', 'info.views.edit_category', name='edit category'),
    url(r'^(?P<category_id>\d+)/new$', 'info.views.edit_page', name='edit category'),
    url(r'^(?P<category_id>\d+)/(?P<page_id>\d+)$', 'info.views.view_page', name='view page'),
    url(r'^(?P<category_id>\d+)/(?P<page_id>\d+)$/edit', 'info.views.edit_page', name='edit page'),
)
