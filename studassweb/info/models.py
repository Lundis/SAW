from django.db import models
from django.contrib.auth.models import User
from menu.models import Menu

class InfoPage(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    text_html = models.TextField()

class InfoPageEdit(models.Model):
    page = models.ForeignKey(InfoPage)
    author = models.ForeignKey(User)
    date = models.DateTimeField('Date edited')

class InfoCategory(models.Model):
    name = models.CharField(max_length=50)
    submenu = models.ForeignKey(Menu)
