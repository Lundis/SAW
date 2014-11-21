from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'info.views.main', name='view categories'),
    url(r'^(?P<category>)/$', 'info.views.view_category', name='view category'),
    url(r'^(?P<category>)/edit$', 'info.views.edit_category', name='edit category'),
    url(r'^(?P<category>)/(?P<page>)$', 'info.views.view_page', name='view page'),
    url(r'^(?P<category>)/(?P<page>)$/edit', 'info.views.edit_page', name='edit page'),
)
