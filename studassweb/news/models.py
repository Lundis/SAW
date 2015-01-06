from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=200)
    # preformatted text used for editing the article
    text = models.TextField()
    # formatted html
    text_html = models.TextField()
    publication_date = models.DateTimeField()
    picture = models.ImageField()
    author = models.ForeignKey(User)


class Category(models.Model):
    name = models.CharField(max_length=100)


class NewsInCategory(models.Model):
    news = models.ForeignKey(News)
    category = models.ForeignKey(Category)


