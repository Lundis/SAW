from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]


class Article(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # A small thumbnail used in the news feed
    picture = models.ImageField(upload_to="news/article_thumbnails")
    author = models.ForeignKey(User)
    categories = models.ManyToManyField(Category, through="ArticleInCategory")

    class Meta:
        ordering = ["-created"]

    def get_summary(self):
        if self.summary is not None or self.summary != "":
            return self.summary
        else:
            return


class ArticleInCategory(models.Model):
    article = models.ForeignKey(Article)
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ["category", "article"]



