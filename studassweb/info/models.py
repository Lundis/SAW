from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class InfoPage(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=500)

class InfoPageEdit(models.Model):
    page = models.ForeignKey(InfoPage)
    author = models.ForeignKey(User)
    date = models.DateTimeField('Date edited')

