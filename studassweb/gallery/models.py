from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.urlresolvers import reverse
# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(default=datetime.datetime.now())
    author = models.ForeignKey(User)
    #Visibility?
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.modified =datetime.datetime.now()
        super(Album, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("gallery.views.view_album", kwargs={'album_id': self.id})

class Photo(models.Model):
    image = models.ImageField()
    album_id = models.ForeignKey(Album)
    author = models.ForeignKey(User)
    description = models.TextField(max_length=300)
    uploaded = models.DateTimeField()

