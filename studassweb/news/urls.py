from django.conf.urls import patterns, url

article_pattern = r'(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w\d]+)'

urlpatterns = patterns('',
    url(r'^$', 'news.views.home', name='news_home'),
    url(r'^view_article/%s$' % article_pattern, 'news.views.view_article', name='news_view_article'),
    url(r'^add_article$', 'news.views.view_article', name='news_add_article'),
    url(r'^edit_article/%s$' % article_pattern, 'news.views.edit_article', name='news_edit_article'),
    url(r'^add_category$', 'news.views.edit_category', name='news_add_article'),
    url(r'^edit_category/(?P<category_id>\d+)$', 'news.views.edit_category', name='news_edit_article'),
)
