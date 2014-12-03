from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Album(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    #Visibility?
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Album, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("gallery.views.view_album", kwargs={'album_id': self.id})


class Photo(models.Model):
    image = models.ImageField()
    album_id = models.ForeignKey(Album)
    author = models.ForeignKey(User)
    description = models.TextField(max_length=300)
    uploaded = models.DateTimeField()

