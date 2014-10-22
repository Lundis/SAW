from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=200)
    text = models.TextField(max_length=2000)
    publication_date = models.DateTimeField()
    picture = models.ImageField()
    #User from member base again?

class Category(models.Model):
    category_id = models.IntegerField()


class NewsInCategory(models.Model):
    news = models.ForeignKey(News)
    category = models.ForeignKey(Category)


