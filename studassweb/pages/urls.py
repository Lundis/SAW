from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'pages.views.main', name='pages_view_categories'),

    url(r'^new_category$', 'pages.views.edit_category', name='pages_new_category'),
    url(r'^category/(?P<slug>[\w-]+)/$', 'pages.views.view_category', name='pages_view_category'),
    url(r'^edit_category/(?P<category_id>\d+)$', 'pages.views.edit_category', name='pages_edit_category'),
    url(r'^delete_category/(?P<category_id>\d+)$', 'pages.views.delete_category', name='pages_delete_category'),

    url(r'^page/(?P<slug>[\w-]+)$', 'pages.views.view_page', name='pages_view_page'),
    url(r'^page/(?P<slug>[\w-]+)/revision/(?P<revision_id>\d+)$', 'pages.views.view_page', name='pages_view_page'),
    url(r'^new_page/(?P<category_id>\d+)$', 'pages.views.edit_page', name='pages_new_page'),
    url(r'^new_page$', 'pages.views.edit_page', name='pages_new_page'),
    url(r'^edit_page/(?P<page_id>\d+)$', 'pages.views.edit_page', name='pages_edit_page'),
    url(r'^edit_page/(?P<page_id>\d+)/(?P<revision_id>\d+)$', 'pages.views.edit_page', name='pages_edit_page'),
    url(r'^revert_page/(?P<revision_id>\d+)$', 'pages.views.revert_page', name='pages_revert_page'),
    url(r'^delete_page/(?P<page_id>\d+)', 'pages.views.delete_page', name='pages_delete_page')
)
