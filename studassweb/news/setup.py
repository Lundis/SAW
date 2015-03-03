from django.contrib.auth.models import User
from .models import NewsSettings, Article


def setup():
    settings = NewsSettings.instance()
    if not settings.is_setup:
        article = Article(title="Hello World!",
                          text="Congratulations on setting up SAW!",
                          author=User.objects.all().first())
        article.save()
        settings.is_setup = True
        settings.save()