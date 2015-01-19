from django.shortcuts import render
from gallery.forms import *
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from users import permissions
import logging

logger = logging.getLogger(__name__)

def view_gallery(request):
    return render(request, 'gallery/view_gallery.html')

def create_album(request, album_id=None):
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:

        album = None

    form = AlbumForm(instance=album)

    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            tmp = form.save()
            return HttpResponseRedirect(reverse('gallery_view_album', kwargs={'album_id': tmp.id}))

    context = {'form': form}
    return render(request, 'gallery/create_album.html', context)

def view_album(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        return render(request, 'gallery/view_album.html', {
            'album': album},)
    except Album.DoesNotExist:
        return HttpResponseNotFound('No album with that id found')

def edit_album(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        return render(request, 'gallery/edit_album.html', {
            'album': album},)
    except Album.DoesNotExist:
        return HttpResponseNotFound('error')

def delete_album(request, album_id):
    if request.method == 'POST':
        try:
            album = Album.objects.get(id=album_id)
            album.delete()
            return HttpResponseRedirect(reverse("gallery_main"))  # TODO give feedback to user
        except Album.DoesNotExist:
            return HttpResponseNotFound('No such album found!')
        except models.ProtectedError:
            return HttpResponseNotFound('You need to remove associated pictures first')
    else:
            logger.warning('Attempted to access delete_album via GET')
            return HttpResponseNotAllowed(['POST', ])

def add_picture(request, photo_id=None):
    form = PictureForm()
    try:
        photo = Photo.objects.get(id=photo_id)
        form = PictureForm(instance=photo)
    except Photo.DoesNotExist:
        photo = None
    if request.method == 'POST':
        form = PictureForm(request.POST, instance=photo)
        if form.is_valid():
            tmp = form.save()
            return HttpResponseRedirect(reverse('gallery_view_picture', kwargs={'photo_id': tmp.id}))

    context = {'form': form}
    return render(request, 'gallery/view_album.html', context)

def view_picture(request, photo_id):
    try:
        photo = Photo.objects.get(id=photo_id)
        return render(request, 'gallery/view_photo.html', {
            'photo': photo},)
    except Photo.DoesNotExist:
        return HttpResponseNotFound('No photo with that id found')

def edit_picture(request, photo_id):
    form = PictureForm()
    try:
        photo = Photo.objects.get(id=photo_id)
        form = PictureForm(instance=photo)
    except Photo.DoesNotExist:
        photo = None
    if request.method == 'POST':
        form = PictureForm(request.POST, instance=photo)
        if form.is_valid():
            tmp = form.save()
            return HttpResponseRedirect(reverse('gallery_view_picture', kwargs={'photo_id': tmp.id}))

    context = {'form': form}
    return render(request, 'gallery/view_photo.html', context)

def delete_picture(request, photo_id):
        if request.method == 'POST':
            try:
                photo = Photo.objects.get(id=photo_id)
                photo.delete()
                return HttpResponseRedirect(reverse("gallery_main"))  #TODO give feedback to user
            except Photo.DoesNotExist:
                return HttpResponseNotFound('No such photo!')
        else:
            logger.warning('Attempted to access delete_picture via GET')
            return HttpResponseNotAllowed(['POST', ])






