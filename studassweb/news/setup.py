# coding=utf-8
from django.contrib.auth.models import User
from .models import NewsSettings, Article
from frontpage.models import FrontPageItem
import logging

logger = logging.getLogger(__name__)


def setup():
    """
    Sets up the
    :return:
    """
    settings = NewsSettings.instance()
    if not settings.is_setup:
        article = Article(title="Hello World!",
                          text="Congratulations on setting up SAW!",
                          author=User.objects.all().first())
        article.save()
        settings.is_setup = True
        settings.save()

    # Make sure that the frontpage item exists
    item, created = FrontPageItem.objects.get_or_create(identifier="news/latest_news")
    if created:
        logger.info("Created News frontpage item")
        item.title = "Latest News"
        item.module = "news"
        item.render_function = "render_latest_news"
        item.save()
