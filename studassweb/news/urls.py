from django.conf.urls import patterns, url

slug_pattern = '(?P<slug>[-\w\d]+)'
article_pattern = r'(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/' + slug_pattern

urlpatterns = patterns('',
    url(r'^$', 'news.views.home', name='news_home'),
    url(r'^article/%s$' % article_pattern, 'news.views.view_article', name='news_view_article'),
    url(r'^add_article$', 'news.views.edit_article', name='news_add_article'),
    url(r'^edit_article/%s$' % article_pattern, 'news.views.edit_article', name='news_edit_article'),
    url(r'^delete_article/%s$' % article_pattern, 'news.views.delete_article', name='news_delete_article'),
    url(r'^category/(?P<category_id>\d+)$', 'news.views.home', name='news_view_category'),
    url(r'^add_category$', 'news.views.edit_category', name='news_add_category'),
    url(r'^edit_category/(?P<category_id>\d+)$', 'news.views.edit_category', name='news_edit_category'),
)
