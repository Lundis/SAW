from django.conf.urls import patterns, url

slug_pattern = '(?P<slug>[-\w\d]+)'
article_pattern = r'(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/' + slug_pattern

urlpatterns = patterns('',
    url(r'^(?P<category_name>([a-zA-Z][a-zA-Z0-9 ]*))/(?P<page>\d+)$', 'news.views.home', name='news_home'),
    url(r'^(?P<page>\d+)$', 'news.views.home', name='news_home'),
    url(r'^(?P<category_name>[a-zA-Z0-9 ]+)$', 'news.views.home', name='news_home'),
    url(r'^$', 'news.views.home', name='news_home'),
    url(r'^article/%s$' % article_pattern, 'news.views.view_article', name='news_view_article'),
    url(r'^add_article$', 'news.views.edit_article', name='news_add_article'),
    url(r'^edit_article/(?P<article_id>\d+)', 'news.views.edit_article', name='news_edit_article'),
    url(r'^delete_article/(?P<article_id>\d+)$', 'news.views.delete_article', name='news_delete_article'),
    url(r'^add_category$', 'news.views.edit_category', name='news_add_category'),
    url(r'^edit_category/(?P<category_id>\d+)$', 'news.views.edit_category', name='news_edit_category'),
    url(r'^delete_category/(?P<category_id>\d+)$', 'news.views.delete_category', name='news_delete_category'),

)
