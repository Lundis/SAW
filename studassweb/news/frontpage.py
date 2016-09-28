# coding=utf-8

from .models import Article, NewsSettings
from django.template import Context
from django.template.loader import get_template


def render_latest_news(context) -> str:
    max_number_of_articles = NewsSettings.instance().number_of_articles_on_frontpage
    articles = Article.objects.all().order_by("-created_date", "-created_time")[0:max_number_of_articles]
    articles_dict = {
        'count': 0,
        'list': []
    }
    for article in articles:
        if article.can_view(context['user']):
            articles_dict['count'] += 1
            articles_dict['list'].append(article)

    context['articles'] = articles_dict
    template = get_template("news/frontpage_content.html")
    return template.render(Context(context))
