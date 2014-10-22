from django.db import models

# Create your models here.
class InfoPage(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=500)

class InfoPageEdit(models.Model):
    page = models.ForeignKey(InfoPage)
    #author is user but unsure from where?
    date = models.DateTimeField('Date edited')

