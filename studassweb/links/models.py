from django.db import models

# Create your models here.


class LinkTo(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    picture = models.ImageField()
