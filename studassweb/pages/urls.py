from django.conf.urls import patterns, url



urlpatterns = patterns('',
    url(r'^$', 'pages.views.main', name='pages_view_categories'),

    url(r'^category/new$', 'pages.views.edit_category', name='pages_new_category'),
    url(r'^category/(?P<slug>[\w-]+)/$', 'pages.views.view_category', name='pages_view_category'),
    url(r'^category/(?P<category_id>\d+)/edit$', 'pages.views.edit_category', name='pages_edit_category'),
    url(r'^category/(?P<category_id>\d+)/delete$', 'pages.views.delete_category', name='pages_delete_category'),

    url(r'^page/(?P<slug>[\w-]+)$', 'pages.views.view_page', name='pages_view_page'),
    url(r'^page/(?P<slug>[\w-]+)/revision/(?P<revision_id>\d+)$', 'pages.views.view_page', name='pages_view_page'),
    url(r'^page/(?P<category_id>\d+)/new$', 'pages.views.edit_page', name='pages_new_page'),
    url(r'^page/(?P<page_id>\d+)/edit$', 'pages.views.edit_page', name='pages_edit_page'),
    url(r'^page/(?P<page_id>\d+)/delete', 'pages.views.delete_page', name='pages_delete_page')
)
