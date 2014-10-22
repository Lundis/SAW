from django.db import models

# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField()
    #User?
    #Visibility?
    modified = models.DateTimeField()

class Photo(models.Model):
    image = models.ImageField()
    album_id = models.ForeignKey(Album)
    #Author?
    description = models.TextField(max_length=300)
    uploaded = models.DateTimeField()