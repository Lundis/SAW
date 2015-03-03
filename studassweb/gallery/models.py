from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
import itertools


class Album(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()  ##this has turned out to be a silly field(?) maybe only for individual pictures
    created = models.DateTimeField(auto_now_add=True) ##same thing, might want for pictures though
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("gallery.views.view_album", kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.name)

    def get_photo_count(self):
        return str(Photo.objects.filter(album_id=self.id).count())

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug and ensure it is unique

            max_length = Album._meta.get_field('slug').max_length
            temp_slug = orig = slugify(self.name)[:max_length]
            for x in itertools.count(1):
                if not Album.objects.filter(slug=temp_slug).exists():
                    break

                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                temp_slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

            self.slug = temp_slug
        super(Album, self).save(*args, **kwargs)


class Photo(models.Model):
    album = models.ForeignKey(Album)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(max_length=300)
    uploaded = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='gallery_files')

    def get_absolute_url(self):
        return reverse("gallery.views.view_picture", kwargs={'photo_id': self.id})

    def __str__(self):
        return self.uploaded.strftime("%Y-%m-%d") + " : " + str(self.album.name)
