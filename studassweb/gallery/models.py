from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField()
    author = models.ForeignKey(User)
    #Visibility?
    modified = models.DateTimeField()

class Photo(models.Model):
    image = models.ImageField()
    album_id = models.ForeignKey(Album)
    author = models.ForeignKey(User)
    description = models.TextField(max_length=300)
    uploaded = models.DateTimeField()