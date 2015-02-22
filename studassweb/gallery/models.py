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

    def __str__(self):
        return str(self.name)

    def get_photo_count(self):
        return str(Photo.objects.filter(album_id=self.id).count())

class Photo(models.Model):
    album_id = models.ForeignKey(Album)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(max_length=300)
    uploaded = models.DateTimeField()

    def get_absolute_url(self):
        return reverse("gallery.views.view_picture", kwargs={'photo_id': self.id})

    def __str__(self):
        return self.uploaded.strftime("%Y-%m-%d") + " : " + str(self.album_id)


class PhotoFile(models.Model):
    image = models.ImageField(upload_to='gallery_files')
    photo_id = models.ForeignKey(Photo)

    def __str__(self):
        return self.image.name

