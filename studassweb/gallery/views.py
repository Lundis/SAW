from django.shortcuts import render
from gallery.forms import *
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
import logging

logger = logging.getLogger(__name__)

def view_gallery(request):
    albums = Album.objects.filter().order_by('name')
    pictures = Photo.objects.filter().order_by('-uploaded')

    return render(request, 'gallery/view_gallery.html', {
        'albums': albums, 'pictures': pictures},)

def view_album(request, album_id):
    try:
        album = Album.objects.get(id=album_id)
        pictures = Photo.objects.filter(album_id = album_id).order_by('-uploaded')
        return render(request, 'gallery/view_album.html', {
            'album': album, 'pictures': pictures},)
    except Album.DoesNotExist:
        logger.warning('Could not find album with id %s', album_id)
        return HttpResponseNotFound('No album with that id found')

def add_edit_album(request, album_id=-1):
    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        album = None
    form = AlbumForm(instance=album)

    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.save()
            return HttpResponseRedirect(reverse('gallery_view_album', kwargs={'album_id': tmp.id}))
    context = {'form': form}
    return render(request, 'gallery/add_edit_album.html', context)

def delete_album(request, album_id):
    if request.method == 'POST':
        try:
            album = Album.objects.get(id=album_id)
            name = str(album)
            album.delete()
            messages.success(request, "Album "+name+" was sucessfully deleted!")
            return HttpResponseRedirect(reverse("gallery_main"))
        except Album.DoesNotExist:
            return HttpResponseNotFound('No such album found!')
    else:
            logger.warning('Attempted to access delete_album via GET')
            return HttpResponseNotAllowed(['POST', ])


def add_edit_picture(request, photo_id=-1):
    form = PictureForm()
    photofile_factory = inlineformset_factory(Photo, PhotoFile, fields=('id', 'image',), extra=1, can_delete=True)
    try:
        photo = Photo.objects.get(id=photo_id)
        form = PictureForm(instance=photo)
        fileformset = photofile_factory(instance=photo, prefix='dynamix')
    except Photo.DoesNotExist:
        fileformset = photofile_factory(prefix='dynamix')
        photo = None

    if request.method == 'POST':
        form = PictureForm(request.POST, instance=photo)

        fileformset = photofile_factory(request.POST, request.FILES, instance=photo, prefix='dynamix')
        if form.is_valid() and fileformset.is_valid():
            tmp_photo = form.save(commit=False)
            tmp_photo.save()

            for obj in fileformset.save(commit=False):
                obj.photo_id = tmp_photo
                obj.save()

            for obj in fileformset.deleted_objects:
                obj.delete()

            return HttpResponseRedirect(reverse("gallery_view_picture", args=[tmp_photo.id]))

    context = {'form': form, 'filesformset': fileformset}
    return render(request, 'gallery/add_edit_photo.html', context)


def view_picture(request, photo_id):
    try:
        photo = Photo.objects.get(id=photo_id)
        images = PhotoFile.objects.filter(photo_id = photo_id)

        return render(request, 'gallery/view_picture.html', {
            'photo': photo, 'images': images},)
    except Photo.DoesNotExist:
        logger.warning('could not find photo with id %s', photo_id)
        return HttpResponseNotFound('No photo with that id found')

def delete_picture(request, photo_id):
        if request.method == 'POST':
            try:
                photo = Photo.objects.get(id=photo_id)
                images = PhotoFile.objects.filter(photo_id=photo_id)
                images.delete()
                photo.delete()
                return HttpResponseRedirect(reverse("gallery_main"))  # TODO give feedback to user
            except Photo.DoesNotExist:
                return HttpResponseNotFound('No such photo!')
        else:
            logger.warning('Attempted to access delete_picture via GET')
            return HttpResponseNotAllowed(['POST', ])






