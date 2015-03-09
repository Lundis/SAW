from django.shortcuts import render
from gallery.forms import *
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
from multiuploader.forms import MultiUploadForm
import logging

logger = logging.getLogger(__name__)


def view_gallery(request):
    albums = Album.objects.order_by('name')
    pictures = Photo.objects.order_by('-uploaded')

    return render(request, 'gallery/view_gallery.html', {
        'albums': albums, 'pictures': pictures},)


def view_album(request, slug):
    try:
        album = Album.objects.get(slug=slug)
        pictures = Photo.objects.filter(album=album).order_by('-uploaded')
        return render(request, 'gallery/view_album.html', {
            'album': album, 'pictures': pictures},)
    except Album.DoesNotExist:
        logger.warning('Could not find album with slug %s', slug)
        return HttpResponseNotFound(_('No album with that id found'))


def add_edit_album(request, slug=None):
    try:
        album = Album.objects.get(slug=slug)
    except Album.DoesNotExist:
        album = None
    form = AlbumForm(instance=album)
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            album = form.save(user=request.user)
            return HttpResponseRedirect(album.get_absolute_url())
    context = {'form': form, }
    return render(request, 'gallery/add_edit_album.html', context)


def delete_album(request, slug):
    if request.method == 'POST':
        try:
            album = Album.objects.get(slug=slug)
            name = str(album)
            album.delete()
            messages.success(request, "Album "+name+" was sucessfully deleted!")
            return HttpResponseRedirect(reverse("gallery_main"))
        except Album.DoesNotExist:
            return HttpResponseNotFound('No such album found!')
    else:
            logger.warning('Attempted to access delete_album via GET')
            return HttpResponseNotAllowed(['POST', ])


def manage_album(request, slug):
    album = Album.objects.get(slug=slug)
    context = {'album': album, 'uploadForm': MultiUploadForm(form_type="images")}
    return render(request, 'gallery/add_edit_photos.html', context)


def delete_picture(request, photo_id):
        if request.method == 'POST':
            try:
                photo = Photo.objects.get(id=photo_id)
                name = str(photo)
                images = Photo.objects.filter(photo_id=photo_id)
                images.delete()
                photo.delete()
                messages.success(request, "Photo "+name+" was sucessfully deleted!")
                return HttpResponseRedirect(reverse("gallery_main"))
            except Photo.DoesNotExist:
                return HttpResponseNotFound('No such photo!')
        else:
            logger.warning('Attempted to access delete_picture via GET')
            return HttpResponseNotAllowed(['POST', ])