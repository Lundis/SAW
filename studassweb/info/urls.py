from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'info.views.main', name='info_view_categories'),
    url(r'^cat/new$', 'info.views.edit_category', name='info_new_category'),
    url(r'^cat/(?P<category_id>\d+)/$', 'info.views.view_category', name='info_view_category'),
    url(r'^cat/(?P<category_id>\d+)/edit$', 'info.views.edit_category', name='info_edit_category'),
    url(r'^cat/(?P<category_id>\d+)/delete$', 'info.views.delete', name='info_delete_category'),
    url(r'^page/(?P<page_id>\d+)$', 'info.views.view_page', name='info_view_page'),
    url(r'^page/(?P<category_id>\d+)/new$', 'info.views.edit_page', name='info_new_page'),
    url(r'^page/(?P<page_id>\d+)/edit$', 'info.views.edit_page', name='info_edit_page'),
    url(r'^page/(?P<page_id>\d+)/delete', 'info.views.delete', name='info_delete_page')
)
